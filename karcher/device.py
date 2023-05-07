# -----------------------------------------------------------
# Copyright (c) 2023 Lauris BH
# SPDX-License-Identifier: MIT
# -----------------------------------------------------------

from dataclasses import dataclass, fields
from enum import Enum
import json
from typing import Any, List

from .consts import Product
from .utils import snake_case


class DeviceStatus(int, Enum):
    """Device status enum."""
    Offline = 0
    Online = 1


@dataclass(init=False)
class DeviceVersion:
    """Device version class.

    This class represents a Karcher Home Robots device version.
    """
    package_type: str = ''
    version: int = 0
    version_name: str = ''
    ctrl_version: str = ''

    def __init__(self, **kwargs):
        names = set([f.name for f in fields(self)])
        for k, v in kwargs.items():
            k = snake_case(k)
            if k in names:
                setattr(self, k, v)


@dataclass
class DevicePropertiesPrivacy:
    """Device privacy properties class."""

    ai_recognize: int = 0
    dirt_recognize: int = 0
    pet_recognize: int = 0
    carpet_turbo: int = 0
    carpet_avoid: int = 0
    carpet_show: int = 0
    auto_upgrade: int = 0
    map_uploads: int = 0
    record_uploads: int = 0


@dataclass
class DevicePropertiesNetwork:
    """Device network status properties class."""

    rssi: str = ''
    loss: int = 0
    ping: int = 0
    ip: str = ''
    mac: str = ''


@dataclass
class DevicePropertiesOrderTotal:
    """Device order total properties class."""

    enable: int = 0
    total: int = 0


@dataclass
class DevicePropertiesQuiet:
    """Device quite status properties class."""

    begin_time: int = 0
    end_time: int = 0
    quiting: int = 0


@dataclass(init=False)
class DeviceProperties:
    """Device properties class.

    This class represents a Karcher Home Robots detailed device properties.
    """

    firmware: str = ''
    firmware_code: int = 0
    status: int = 0
    fault: int = 0
    wind: int = 0
    water: int = 0
    mode: int = 0
    quantity: int = 0
    alarm: int = 0
    volume: int = 0
    hypa: int = 0
    main_brush: int = 0
    side_brush: int = 0
    mop_life: int = 0
    net_status: DevicePropertiesNetwork = DevicePropertiesNetwork()
    repeat_state: int = 0
    tank_state: int = 0
    cloth_state: int = 0
    sweep_type: int = 0
    mop_route: int = 0
    time_zone: int = 0
    language: int = 0
    cleaning_time: int = 0
    cleaning_area: int = 0
    custom_type: int = 0
    sound: int = 0
    work_mode: int = 0
    tank_shake: int = 0
    shake_shift: int = 0
    electrolysis: int = 0
    station_act: int = 0
    charge_state: int = 0
    back_to_wash: int = 0
    break_charging: int = 0
    order_total: DevicePropertiesOrderTotal = DevicePropertiesOrderTotal()
    memory_map: int = 0
    current_map_id: int = 0
    map_num: int = 0
    has_new_map: int = 0
    build_map: int = 0
    quiet_is_open: int = 0
    quiet_begin_time: int = 0
    quiet_end_time: int = 0
    broken_clean: int = 0
    privacy: DevicePropertiesPrivacy = DevicePropertiesPrivacy()
    cur_path: List[float]
    dust_action: int = 0
    voice_type: int = 0
    quiet_status: DevicePropertiesQuiet = DevicePropertiesQuiet()
    last_update_time: int = 0

    def __init__(self, **kwargs):
        setattr(self, 'cur_path', [])
        self.update(kwargs)

    def update(self, data: dict[str, Any]) -> bool:
        """Update device properties."""

        updated = False
        names = set([f.name for f in fields(self)])
        for k, v in data.items():
            if k in names:
                if k == 'firmware_code':
                    v = int(v)
                if v != getattr(self, k):
                    setattr(self, k, v)
                    updated = True
        return updated


@dataclass(init=False)
class Device:
    """Device class.

    This class represents a Karcher Home Robots device.
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
