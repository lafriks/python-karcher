# -----------------------------------------------------------
# Copyright (c) 2023 Lauris BH
# SPDX-License-Identifier: MIT
# -----------------------------------------------------------

import base64
from dataclasses import dataclass, fields
import json


@dataclass(init=False)
class Domains:
    """Domains URLs class.

    This class represents a Karcher Home access URLs.
    """
    app_api: str
    mqtt: str

    def __init__(self, **kwargs):
        names = set([f.name for f in fields(self)])
        for k, v in kwargs.items():
            k = k.lower()
            if k in names:
                if k == 'app_api':
                    v = 'https://' + v
                setattr(self, k, v)


@dataclass(init=False)
class Session:
    """Authorized user session class.

    This class represents a Karcher Home authorized user session.
    """

    register_id: str
    user_id: str
    auth_token: str
    mqtt_token: str

    def __init__(self, **kwargs):
        names = set([f.name for f in fields(self)])
        if 'id' in kwargs:
            setattr(self, 'user_id', kwargs['id'])
        if 'data' in kwargs:
            kwargs = kwargs['data']
        for k, v in kwargs.items():
            k = k.lower()
            if k == 'auth':
                k = 'auth_token'
            elif k == 'emq_token':
                k = 'mqtt_token'
            if k in names:
                setattr(self, k, v)

    def reset(self):
        """Reset session."""
        self.user_id = ''
        self.auth_token = ''
        self.mqtt_token = ''

    @staticmethod
    def from_token(auth_token: str, mqtt_token: str):
        """Create session from auth and MQTT tokens."""
        sess = Session()

        # Get user ID from auth token
        token_data = auth_token.split(".")[1]
        missing_padding = len(token_data) % 4
        if missing_padding:
            token_data += '=' * (4 - missing_padding)
        data = json.loads(base64.b64decode(token_data))
        auth = json.loads(data["value"])

        sess.user_id = auth["id"]
        sess.auth_token = auth_token
        sess.mqtt_token = mqtt_token

        return sess
