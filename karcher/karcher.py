# -----------------------------------------------------------
# Copyright (c) 2023 Lauris BH
# SPDX-License-Identifier: MIT
# -----------------------------------------------------------

import asyncio
import collections
import json
import threading
from typing import List, Any
import aiohttp
import urllib.parse

from .auth import Domains, Session
from .countries import get_country_code, get_region_by_country
from .consts import (
    APP_VERSION_CODE, APP_VERSION_NAME, PROJECT_TYPE, PROTOCOL_VERSION,
    REGION_URLS, ROBOT_PROPERTIES, SSL_CERTIFICATE_THUMBPRINT, TENANT_ID,
    Language, Region
)
from .device import Device, DeviceProperties
from .exception import KarcherHomeAccessDenied, KarcherHomeException, handle_error_code
from .map import Map
from .mqtt import MqttClient, get_device_topic_property_get_reply, get_device_topics
from .user import UserProfile
from .utils import (
    decrypt, decrypt_map, encrypt, get_nonce, get_random_string,
    get_timestamp, get_timestamp_ms, is_email, md5
)


class KarcherHome:
    """Main class to access Karcher Home Robots API"""

    @classmethod
    async def create(
            cls,
            country: str = 'GB',
            language: Language = Language.EN,
            session: aiohttp.ClientSession = None):
        """Create Karcher Home Robots API instance"""

        self = KarcherHome()
        self._country = country.upper()
        self._base_url = REGION_URLS[get_region_by_country(self._country)]
        self._language = language

        if session is not None:
            self._http_external = True
            self._http = session

        data = await self.get_urls()
        # Update base URLs
        if data.app_api != '':
            self._base_url = data.app_api
        if data.mqtt != '':
            self._mqtt_url = data.mqtt

        return self

    def __init__(self):
        """Initialize Karcher Home Robots API"""

        super().__init__()
        self._country = 'US'
        self._base_url = REGION_URLS[Region.US]
        self._mqtt_url = None
        self._language = Language.EN
        self._session = None
        self._mqtt = None
        self._device_props = {}
        self._wait_events = {}
        self._http = None
        self._http_external = False

    def __del__(self):
        """Destructor"""

        asyncio.run(self.close())

    async def close(self):
        """Close underlying connections"""

        if self._mqtt is not None:
            self._mqtt.disconnect()
            self._mqtt = None

        if self._http is not None:
            if not self._http_external:
                await self._http.close()
            self._http = None

    async def _request(self, method: str, url: str, **kwargs) -> aiohttp.ClientResponse:
        if self._http is None:
            self._http_external = False
            self._http = aiohttp.ClientSession()

        headers = {}
        if kwargs.get('headers') is not None:
            headers = kwargs['headers']

        headers['User-Agent'] = 'Android_' + TENANT_ID
        auth = ''
        if self._session is not None and self._session.auth_token != '':
            auth = self._session.auth_token
            headers['authorization'] = auth
        if self._session is not None and self._session.user_id != '':
            headers['id'] = self._session.user_id
        headers['tenantId'] = TENANT_ID

        # Sign request
        nonce = get_nonce()
        ts = str(get_timestamp())
        data = ''
        if method == 'GET':
            params = kwargs.get('params') or {}
            if type(params) == str:
                params = urllib.parse.parse_qs(params)
            buf = urllib.parse.urlencode(params)
            data = buf
            kwargs['params'] = buf
        elif method == 'POST' or method == 'PUT':
            v = params = kwargs.get('json') or {}
            if type(v) == dict:
                v = collections.OrderedDict(v.items())
                for key, val in v.items():
                    data += key
                    if val is None:
                        data += 'null'
                    elif type(val) == str:
                        data += val
                    elif type(val) == dict:
                        data += json.dumps(val, separators=(',', ':'))
                    else:
                        data += str(val)
                kwargs['json'] = v

        headers['sign'] = md5(auth + ts + nonce + data)
        headers['ts'] = ts
        headers['nonce'] = nonce

        kwargs['headers'] = headers
        kwargs['ssl'] = aiohttp.Fingerprint(SSL_CERTIFICATE_THUMBPRINT)
        return await self._http.request(method, self._base_url + url, **kwargs)

    async def _download(self, url) -> bytes:
        headers = {
            'User-Agent': 'Android_' + TENANT_ID,
        }

        resp = await self._http.get(url, headers=headers)
        if resp.status != 200:
            raise KarcherHomeException(-1,
                                       'HTTP error: ' + str(resp.status_code))

        data = await resp.content.read(-1)
        resp.close()

        return data

    async def _process_response(self, resp: aiohttp.ClientResponse, prop=None) -> Any:
        if resp.status != 200:
            resp.close()
            raise KarcherHomeException(-1,
                                       'HTTP error: ' + str(resp.status))
        data = await resp.json()
        resp.close()

        # Check for error response
        if data['code'] != 0:
            handle_error_code(data['code'], data['msg'])
        # Check for empty response
        if 'result' not in data:
            return None
        # Handle special response types
        result = data['result']
        if type(result) == str:
            raise KarcherHomeException(-2, 'Invalid response: ' + result)
        if prop is not None:
            return json.loads(decrypt(result[prop]))
        return result

    def _mqtt_connect(self, wait_for_connect=False):
        if self._session is None \
                or self._session.mqtt_token == '' or self._session.user_id == '':
            raise KarcherHomeAccessDenied('Not authorized')

        if self._mqtt is not None:
            return

        u = urllib.parse.urlparse("//" + self._mqtt_url)

        self._mqtt = MqttClient(
            host=u.hostname,
            port=u.port,
            username=self._session.user_id,
            password=self._session.mqtt_token)

        # Special logic for waiting for connection
        event = None
        if wait_for_connect:
            event = threading.Event()
            self._mqtt.on_connect = lambda: event.set()

        self._mqtt.connect()
        self._mqtt.on_message = self._process_mqtt_message

        if wait_for_connect:
            event.wait()
            self._mqtt.on_connect = None

    async def get_urls(self) -> Domains:
        """Get URLs for API and MQTT."""

        resp = await self._request('GET', '/network-service/domains/list', params={
            'tenantId': TENANT_ID,
            'productModeCode': PROJECT_TYPE,
            'version': PROTOCOL_VERSION,
        })

        data = await self._process_response(resp, 'domain')
        return Domains(**data)

    async def login(self, username, password, register_id=None) -> Session:
        """Login using provided credentials."""

        if register_id is None or register_id == '':
            register_id = get_random_string(19)

        if not is_email(username):
            username = '86-' + username

        resp = await self._request('POST', '/user-center/auth/login', json={
            'tenantId': TENANT_ID,
            'lang': str(self._language),
            'token': None,
            'userId': None,
            'password': encrypt(password),
            'username': encrypt(username),
            'authcode': None,
            'projectType': PROJECT_TYPE,
            'versionCode': APP_VERSION_CODE,
            'versionName': APP_VERSION_NAME,
            'phoneBrand': encrypt('xiaomi_mi 9'),
            'phoneSys': 1,
            'noticeSetting': {
                'andIpad': register_id,
                'android': register_id,
            },
        })

        data = await self._process_response(resp)
        self._session = Session(**data)
        self._session.register_id = register_id

        return self._session

    def login_token(
            self,
            auth_token: str,
            mqtt_token: str,
            register_id=None) -> Session:
        """Login using provided tokens."""

        if register_id is None or register_id == '':
            register_id = get_random_string(19)

        self._session = Session.from_token(auth_token, mqtt_token)
        self._session.register_id = register_id

        return self._session

    async def logout(self):
        """End current session.

        This will also reset the session object.
        """
        if self._session is None \
                or self._session.auth_token == '' or self._session.user_id == '':
            self._session = None
            return

        await self._process_response(await self._request(
            'POST', '/user-center/auth/logout'))
        self._session = None

        await self.close()

    async def get_user_info(self) -> UserProfile:
        """Get user profile information."""

        if self._session is None \
                or self._session.auth_token == '' or self._session.user_id == '':
            raise KarcherHomeAccessDenied('Not authorized')

        resp = await self._request(
            'GET',
            '/user-center/app/user/profile')
        data = await self._process_response(resp)

        return UserProfile(**data)

    async def get_devices(self) -> List[Device]:
        """Get all user devices."""

        if self._session is None \
                or self._session.auth_token == '' or self._session.user_id == '':
            raise KarcherHomeAccessDenied('Not authorized')

        resp = await self._request(
            'GET',
            '/smart-home-service/smartHome/user/getDeviceInfoByUserId/'
            + self._session.user_id)

        return [Device(**d) for d in await self._process_response(resp)]

    async def get_map_data(self, dev: Device, map: int = 1):
        # <tenantId>/<modeType>/<deviceSn>/01-01-2022/map/temp/0046690461_<deviceSn>_1
        mapDir = TENANT_ID + '/' + dev.product_mode_code + '/' +\
            dev.sn + '/01-01-2022/map/temp/0046690461_' + \
            dev.sn + '_' + str(map)

        resp = await self._request('POST',
                                   '/storage-management/storage/aws/getAccessUrl',
                                   json={
                                       'dir': mapDir,
                                       'countryCode': get_country_code(self._country),
                                       'serviceType': 2,
                                       'tenantId': TENANT_ID,
                                   })

        data = await self._process_response(resp)
        downloadUrl = data['url']
        if 'cdnDomain' in data and data['cdnDomain'] != '':
            downloadUrl = 'https://' + data['cdnDomain'] + '/' + data['dir']

        data = await self._download(downloadUrl)
        data = decrypt_map(dev.sn, dev.mac, dev.product_id, data)
        if map == 1 or map == 2:
            return Map.parse(data)
        else:
            return json.loads(data)

    def subscribe_device(self, dev: Device):
        """Subscribe to device real-time events."""

        if self._session is None \
                or self._session.mqtt_token == '' or self._session.user_id == '':
            raise KarcherHomeAccessDenied('Not authorized')

        self._mqtt_connect()
        self._device_props[dev.sn] = DeviceProperties()
        self._mqtt.subscribe(get_device_topics(dev.product_id, dev.sn))

    def unsubscribe_device(self, dev: Device):
        """Unsubscribe from device real-time events."""

        if self._session is None \
                or self._session.mqtt_token == '' or self._session.user_id == '':
            return

        if self._mqtt is None or dev.sn not in self._device_props:
            return

        self._mqtt.unsubscribe(get_device_topics(dev.product_id, dev.sn))
        del self._device_props[dev.sn]

    def _process_mqtt_message(self, topic, msg):
        sn = None
        for s in self._device_props.keys():
            if '/' + s + '/' in topic:
                sn = s
                break

        if sn is None:
            # Ignore messages for devices we have not subscribed to
            if topic in self._wait_events:
                self._wait_events[topic].set()
            return

        if 'thing/event/property/post' in topic \
                or 'thing/event/cur_path/post' in topic \
                or 'upgrade/post' in topic:
            if topic in self._wait_events:
                self._wait_events[topic].set()
            return

        if 'thing/service/property/get_reply' in topic:
            data = json.loads(msg)
            if data['code'] != 0:
                # TODO: handle error
                return
            self._update_device_properties(sn, data['data'])
            if topic in self._wait_events:
                self._wait_events[topic].set()
            return

        if topic in self._wait_events:
            self._wait_events[topic].set()

    def _wait_for_topic(self, topic: str, timeout: float = 5):
        if self._mqtt is None:
            return

        if topic in self._wait_events:
            return

        event = threading.Event()
        self._wait_events[topic] = event

        event.wait(timeout)
        del self._wait_events[topic]

    def _update_device_properties(self, sn: str, data: dict):
        if sn not in self._device_props:
            return

        self._device_props[sn].update(data)
        self._device_props[sn].last_update_time = get_timestamp()

    def request_device_update(self, dev: Device):
        """Request device update."""

        if self._session is None \
                or self._session.mqtt_token == '' or self._session.user_id == '':
            raise KarcherHomeAccessDenied('Not authorized')

        self._mqtt_connect()
        self._mqtt.publish(
            "/mqtt/" + dev.product_id + '/' + dev.sn + "/thing/service/property/get",
            json.dumps({
                "method": "prop.get",
                "msgId": str(get_timestamp_ms()),
                "tenantId": TENANT_ID,
                "version": "3.0",
                "params": {
                    "property": ROBOT_PROPERTIES,
                },
            }))

    def get_device_properties(self, dev: Device) -> DeviceProperties:
        """Get device properties if it has subscription."""

        if dev.sn in self._device_props:
            return self._device_props[dev.sn]

        if self._session is None \
                or self._session.mqtt_token == '' or self._session.user_id == '':
            raise KarcherHomeAccessDenied('Not authorized')

        self._mqtt_connect(wait_for_connect=True)
        subscr = dev.sn not in self._device_props
        if subscr:
            self.subscribe_device(dev)
        self.request_device_update(dev)
        self._wait_for_topic(
            get_device_topic_property_get_reply(dev.product_id, dev.sn))

        props = self._device_props[dev.sn]

        if subscr:
            self.unsubscribe_device(dev)

        return props
