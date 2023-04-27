# -----------------------------------------------------------
# Copyright (c) 2023 Lauris BH
# SPDX-License-Identifier: MIT
# -----------------------------------------------------------

from enum import Enum


class Region(str, Enum):
    """Region enum.

    Cloud region.
    """
    EU = 'eu'
    US = 'us'
    CN = 'cn'


class Language(int, Enum):
    """Language enum.

    Language of the API.
    """
    CN = 1
    EN = 2
    ES = 3
    DE = 4
    FR = 5
    PL = 6
    IT = 7
    TR = 12
    CS = 15
    NL = 16
    SV = 17

    def __str__(self):
        if self == Language.CN:
            return 'cn'
        elif self == Language.EN:
            return 'en'
        elif self == Language.ES:
            return 'es'
        elif self == Language.DE:
            return 'de'
        elif self == Language.FR:
            return 'fr'
        elif self == Language.PL:
            return 'pl'
        elif self == Language.IT:
            return 'it'
        elif self == Language.TR:
            return 'tr'
        elif self == Language.CS:
            return 'cs'
        elif self == Language.NL:
            return 'nl'
        elif self == Language.SV:
            return 'sv'
        else:
            return 'en'


class Product(str, Enum):
    """Product model enum."""

    RCV3 = '1528986273083777024'
    RCV5 = '1540149850806333440'
    RCF5 = '1599715149861306368'


REGION_URLS = {
    Region.EU: 'https://eu-appaiot.3irobotix.net',
    Region.US: 'https://us-appaiot.3irobotix.net',
    Region.CN: 'https://cn-appaiot.3irobotix.net',
}

REGION_INDEX = {
    Region.EU: 1,
    Region.US: 2,
    Region.CN: 0,
}

ROBOT_PROPERTIES = [
    'status',
    'firmware_code',
    'firmware',
    'fault',
    'mode',
    'wind',
    'water',
    'repeat_state',
    'charge_state',
    'quantity',
    'work_mode',
    'sweep_type',
    'build_map',
    'cleaning_area',
    'cleaning_time',
    'current_map_id',
    'custom_type',
    'privacy',
    'alarm',
    'volume',
    'tank_state',
    'cloth_state',
    'mop_route',
    'map_num',
    'language',
    'voice_type',
    'quiet_status',
    'quiet_is_open'
]

TENANT_ID = '1528983614213726208'
PROJECT_TYPE = 'android_iot.karcher'
PROTOCOL_VERSION = 'v1'
APP_VERSION_CODE = 10004
APP_VERSION_NAME = '1.0.4'
