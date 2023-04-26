# -----------------------------------------------------------
# Copyright (c) 2023 Lauris BH
# SPDX-License-Identifier: MIT
# -----------------------------------------------------------

from dataclasses import dataclass, fields
from enum import Enum
import json
from typing import List

from .consts import Product
from .utils import snake_case

class DeviceStatus(int, Enum):
    """Device status enum."""
    Offline = 0
    Online = 1

@dataclass(init=False)
class DeviceVersion:
    """Device version class.

    This class represents a Karcher Home device version.
    """
    package_type: str
    version: int
    version_name: str
    ctrl_version: str

    def __init__(self, **kwargs):
        names = set([f.name for f in fields(self)])
        for k, v in kwargs.items():
            k = snake_case(k)
            if k in names:
                setattr(self, k, v)

@dataclass(init=False)
class Device:
    """Device class.

    This class represents a Karcher Home device.
    """

    device_id: str
    sn: str
    mac: str
    nickname: str
    versions: List[DeviceVersion]
    status: DeviceStatus
    is_default: bool
    is_selected: bool
    is_shared: bool
    online_time: int
    photo_url: str
    product_id: Product
    product_mode_code: str
    bind_time: int
    room_id: str

    def __init__(self, **kwargs):
        # Set default values
        for k, v in [('isSelected', False), ('isShare', False), ('isDefault', False)]:
            if k not in kwargs:
                kwargs[k] = v

        names = set([f.name for f in fields(self)])
        for k, v in kwargs.items():
            k = snake_case(k)
            if k == 'is_share':
                k = 'is_shared'
            if k in names:
                if k == 'status':
                    v = DeviceStatus(v)
                if k == 'product_id':
                    v = Product(v)
                elif k == 'versions':
                    v = json.loads(v)
                    v = [DeviceVersion(**x) for x in v]
                setattr(self, k, v)

    def is_online(self):
        """Get device status."""
        return self.status == DeviceStatus.Online
