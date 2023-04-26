# -----------------------------------------------------------
# Copyright (c) 2023 Lauris BH
# SPDX-License-Identifier: MIT
# -----------------------------------------------------------

from google.protobuf.json_format import MessageToDict

from . import mapdata_pb2
from .utils import snake_case, snake_case_fields


class Map:
    @staticmethod
    def parse(data: bytes):
        m = Map()
        rm = mapdata_pb2.RobotMap()
        rm.ParseFromString(data)
        d = {}
        for k, v in MessageToDict(rm).items():
            if k == 'mapData':
                v = v['mapData']
            v = snake_case_fields(v)
            d[snake_case(k)] = v
        setattr(m, 'data', d)
        return m
