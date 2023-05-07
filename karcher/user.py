# -----------------------------------------------------------
# Copyright (c) 2023 Lauris BH
# SPDX-License-Identifier: MIT
# -----------------------------------------------------------

from dataclasses import dataclass, fields

from .utils import decrypt, snake_case

@dataclass(init=False)
class UserProfile:
    """User profile class.

    This class represents a Karcher Home Robots user profile.
    """
    nickname: str = ''
    avatar_url: str = ''
    email: str = ''
    phone: str = ''
    device: int = 0

    def __init__(self, **kwargs):
        names = set([f.name for f in fields(self)])
        for k, v in kwargs.items():
            if k == 'nickName':
                k = 'nickname'
            else:
                k = snake_case(k)
            if k in names:
                if k in ('email', 'phone'):
                    v = decrypt(v)
                setattr(self, k, v)
