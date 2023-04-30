from typing import List
import ssl
from paho.mqtt.client import Client, MQTTv311

from .utils import get_random_device_id


class MqttClient:
    def __init__(self, host, port, username, password):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._topics = []
        self._client = Client(
            client_id=self._username + '_' + get_random_device_id(),
            clean_session=True,
            protocol=MQTTv311)
        self.on_message = None
        self.on_connect = None

    def connect(self):
        # TODO validate certificate
        self._client.tls_set(cert_reqs=ssl.CERT_NONE)
        self._client.tls_insecure_set(True)
        self._client.username_pw_set(self._username, self._password)
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        # TODO: add option to enable logging
        # self._client.on_log = lambda client, userdata, level, buf: print(buf)
        self._client.connect(self._host, self._port, 60)
        self._client.loop_start()

    def disconnect(self):
        self._client.loop_stop()
        self._client.disconnect()

    def _subscribe(self, topics):
        if len(topics) == 0:
            return
        t = []
        for topic in topics:
            t.append((topic, 0))
        self._client.subscribe(t)

    def subscribe(self, topics):
        t = []
        for topic in topics:
            if topic not in self._topics:
                self._topics.append(topic)
                t.append(topic)
        if self._client.is_connected():
            self._subscribe(t)

    def unsubscribe(self, topics):
        t = []
        for topic in topics:
            if topic in self._topics:
                self._topics.remove(topic)
                t.append(topic)
        if self._client.is_connected():
            self._client.unsubscribe(t)

    def publish(self, topic, payload):
        self._client.publish(topic, payload)

    def _on_connect(self, client, userdata, flags, rc):
        self._subscribe(self._topics)
        if self.on_connect is not None:
            self.on_connect()

    def _on_message(self, client, userdata, msg):
        if self.on_message is not None:
            self.on_message(msg.topic, msg.payload)

    def __del__(self):
        self.disconnect()


def get_device_topics(product_id: str, sn: str) -> List[str]:
    return [
        '/mqtt/' + product_id + '/' + sn + '/thing/event/property/post',
        '/mqtt/' + product_id + '/' + sn + '/thing/service/property/set_reply',
        get_device_topic_property_get_reply(product_id, sn),
        '/mqtt/' + product_id + '/' + sn + '/thing/service_invoke',
        '/mqtt/' + product_id + '/' + sn + '/thing/service_invoke_reply/#',
        '/mqtt/' + product_id + '/' + sn + '/thing/event/cur_path/post',
        '/mqtt/' + product_id + '/' + sn + '/ota/service/upgrade/set_reply',
        '/mqtt/' + product_id + '/' + sn + '/ota/service/upgrade/post',
        '/mqtt/' + product_id + '/' + sn + '/ota/service/upgrade/get_reply',
        '/mqtt/' + product_id + '/' + sn + '/ota/service/version/post',
    ]


def get_device_topic_property_get_reply(product_id: str, sn: str) -> str:
    return '/mqtt/' + product_id + '/' + sn + '/thing/service/property/get_reply'
