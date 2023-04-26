from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MapExtInfo(_message.Message):
    __slots__ = ["taskBeginDate", "mapUploadDate", "mapValid", "angle"]
    TASKBEGINDATE_FIELD_NUMBER: _ClassVar[int]
    MAPUPLOADDATE_FIELD_NUMBER: _ClassVar[int]
    MAPVALID_FIELD_NUMBER: _ClassVar[int]
    ANGLE_FIELD_NUMBER: _ClassVar[int]
    taskBeginDate: int
    mapUploadDate: int
    mapValid: int
    angle: float
    def __init__(self, taskBeginDate: _Optional[int] = ..., mapUploadDate: _Optional[int] = ..., mapValid: _Optional[int] = ..., angle: _Optional[float] = ...) -> None: ...

class MapHeadInfo(_message.Message):
    __slots__ = ["mapHeadId", "sizeX", "sizeY", "minX", "minY", "maxX", "maxY", "resolution"]
    MAPHEADID_FIELD_NUMBER: _ClassVar[int]
    SIZEX_FIELD_NUMBER: _ClassVar[int]
    SIZEY_FIELD_NUMBER: _ClassVar[int]
    MINX_FIELD_NUMBER: _ClassVar[int]
    MINY_FIELD_NUMBER: _ClassVar[int]
    MAXX_FIELD_NUMBER: _ClassVar[int]
    MAXY_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    mapHeadId: int
    sizeX: int
    sizeY: int
    minX: float
    minY: float
    maxX: float
    maxY: float
    resolution: float
    def __init__(self, mapHeadId: _Optional[int] = ..., sizeX: _Optional[int] = ..., sizeY: _Optional[int] = ..., minX: _Optional[float] = ..., minY: _Optional[float] = ..., maxX: _Optional[float] = ..., maxY: _Optional[float] = ..., resolution: _Optional[float] = ...) -> None: ...

class MapDataInfo(_message.Message):
    __slots__ = ["mapData"]
    MAPDATA_FIELD_NUMBER: _ClassVar[int]
    mapData: bytes
    def __init__(self, mapData: _Optional[bytes] = ...) -> None: ...

class AllMapInfo(_message.Message):
    __slots__ = ["mapHeadId", "mapName"]
    MAPHEADID_FIELD_NUMBER: _ClassVar[int]
    MAPNAME_FIELD_NUMBER: _ClassVar[int]
    mapHeadId: int
    mapName: str
    def __init__(self, mapHeadId: _Optional[int] = ..., mapName: _Optional[str] = ...) -> None: ...

class DeviceCoverPointDataInfo(_message.Message):
    __slots__ = ["update", "x", "y"]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    update: int
    x: float
    y: float
    def __init__(self, update: _Optional[int] = ..., x: _Optional[float] = ..., y: _Optional[float] = ...) -> None: ...

class DeviceHistoryPoseInfo(_message.Message):
    __slots__ = ["poseId", "points"]
    POSEID_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    poseId: int
    points: _containers.RepeatedCompositeFieldContainer[DeviceCoverPointDataInfo]
    def __init__(self, poseId: _Optional[int] = ..., points: _Optional[_Iterable[_Union[DeviceCoverPointDataInfo, _Mapping]]] = ...) -> None: ...

class DevicePoseDataInfo(_message.Message):
    __slots__ = ["x", "y", "phi"]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    PHI_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    phi: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., phi: _Optional[float] = ...) -> None: ...

class DeviceCurrentPoseInfo(_message.Message):
    __slots__ = ["poseId", "update", "x", "y", "phi"]
    POSEID_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    PHI_FIELD_NUMBER: _ClassVar[int]
    poseId: int
    update: int
    x: float
    y: float
    phi: float
    def __init__(self, poseId: _Optional[int] = ..., update: _Optional[int] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., phi: _Optional[float] = ...) -> None: ...

class DevicePointInfo(_message.Message):
    __slots__ = ["x", "y"]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ...) -> None: ...

class DeviceAreaDataInfo(_message.Message):
    __slots__ = ["status", "type", "areaIndex", "points"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    AREAINDEX_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    status: int
    type: int
    areaIndex: int
    points: _containers.RepeatedCompositeFieldContainer[DevicePointInfo]
    def __init__(self, status: _Optional[int] = ..., type: _Optional[int] = ..., areaIndex: _Optional[int] = ..., points: _Optional[_Iterable[_Union[DevicePointInfo, _Mapping]]] = ...) -> None: ...

class DeviceNavigationPointDataInfo(_message.Message):
    __slots__ = ["pointId", "status", "pointType", "x", "y", "phi"]
    POINTID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    POINTTYPE_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    PHI_FIELD_NUMBER: _ClassVar[int]
    pointId: int
    status: int
    pointType: int
    x: float
    y: float
    phi: float
    def __init__(self, pointId: _Optional[int] = ..., status: _Optional[int] = ..., pointType: _Optional[int] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., phi: _Optional[float] = ...) -> None: ...

class CleanPerferenceDataInfo(_message.Message):
    __slots__ = ["cleanMode", "waterLevel", "windPower", "twiceClean"]
    CLEANMODE_FIELD_NUMBER: _ClassVar[int]
    WATERLEVEL_FIELD_NUMBER: _ClassVar[int]
    WINDPOWER_FIELD_NUMBER: _ClassVar[int]
    TWICECLEAN_FIELD_NUMBER: _ClassVar[int]
    cleanMode: int
    waterLevel: int
    windPower: int
    twiceClean: int
    def __init__(self, cleanMode: _Optional[int] = ..., waterLevel: _Optional[int] = ..., windPower: _Optional[int] = ..., twiceClean: _Optional[int] = ...) -> None: ...

class RoomDataInfo(_message.Message):
    __slots__ = ["roomId", "roomName", "roomTypeId", "meterialId", "cleanState", "roomClean", "roomCleanIndex", "roomNamePost", "cleanPerfer", "colorId"]
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    ROOMNAME_FIELD_NUMBER: _ClassVar[int]
    ROOMTYPEID_FIELD_NUMBER: _ClassVar[int]
    METERIALID_FIELD_NUMBER: _ClassVar[int]
    CLEANSTATE_FIELD_NUMBER: _ClassVar[int]
    ROOMCLEAN_FIELD_NUMBER: _ClassVar[int]
    ROOMCLEANINDEX_FIELD_NUMBER: _ClassVar[int]
    ROOMNAMEPOST_FIELD_NUMBER: _ClassVar[int]
    CLEANPERFER_FIELD_NUMBER: _ClassVar[int]
    COLORID_FIELD_NUMBER: _ClassVar[int]
    roomId: int
    roomName: str
    roomTypeId: int
    meterialId: int
    cleanState: int
    roomClean: int
    roomCleanIndex: int
    roomNamePost: DevicePointInfo
    cleanPerfer: CleanPerferenceDataInfo
    colorId: int
    def __init__(self, roomId: _Optional[int] = ..., roomName: _Optional[str] = ..., roomTypeId: _Optional[int] = ..., meterialId: _Optional[int] = ..., cleanState: _Optional[int] = ..., roomClean: _Optional[int] = ..., roomCleanIndex: _Optional[int] = ..., roomNamePost: _Optional[_Union[DevicePointInfo, _Mapping]] = ..., cleanPerfer: _Optional[_Union[CleanPerferenceDataInfo, _Mapping]] = ..., colorId: _Optional[int] = ...) -> None: ...

class DeviceRoomMatrix(_message.Message):
    __slots__ = ["matrix"]
    MATRIX_FIELD_NUMBER: _ClassVar[int]
    matrix: bytes
    def __init__(self, matrix: _Optional[bytes] = ...) -> None: ...

class DeviceChainPointDataInfo(_message.Message):
    __slots__ = ["x", "y", "value"]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    value: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...

class DeviceRoomChainDataInfo(_message.Message):
    __slots__ = ["roomId", "points"]
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    roomId: int
    points: _containers.RepeatedCompositeFieldContainer[DeviceChainPointDataInfo]
    def __init__(self, roomId: _Optional[int] = ..., points: _Optional[_Iterable[_Union[DeviceChainPointDataInfo, _Mapping]]] = ...) -> None: ...

class ObjectDataInfo(_message.Message):
    __slots__ = ["objectId", "objectTypeId", "objectName", "confirm", "x", "y", "url"]
    OBJECTID_FIELD_NUMBER: _ClassVar[int]
    OBJECTTYPEID_FIELD_NUMBER: _ClassVar[int]
    OBJECTNAME_FIELD_NUMBER: _ClassVar[int]
    CONFIRM_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    objectId: int
    objectTypeId: int
    objectName: str
    confirm: int
    x: float
    y: float
    url: str
    def __init__(self, objectId: _Optional[int] = ..., objectTypeId: _Optional[int] = ..., objectName: _Optional[str] = ..., confirm: _Optional[int] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., url: _Optional[str] = ...) -> None: ...

class FurnitureDataInfo(_message.Message):
    __slots__ = ["id", "typeId", "points", "url"]
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPEID_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    id: int
    typeId: int
    points: _containers.RepeatedCompositeFieldContainer[DevicePointInfo]
    url: str
    def __init__(self, id: _Optional[int] = ..., typeId: _Optional[int] = ..., points: _Optional[_Iterable[_Union[DevicePointInfo, _Mapping]]] = ..., url: _Optional[str] = ...) -> None: ...

class HouseInfo(_message.Message):
    __slots__ = ["id", "name", "curMapCount", "maxMapSize", "maps"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CURMAPCOUNT_FIELD_NUMBER: _ClassVar[int]
    MAXMAPSIZE_FIELD_NUMBER: _ClassVar[int]
    MAPS_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    curMapCount: int
    maxMapSize: int
    maps: _containers.RepeatedCompositeFieldContainer[AllMapInfo]
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., curMapCount: _Optional[int] = ..., maxMapSize: _Optional[int] = ..., maps: _Optional[_Iterable[_Union[AllMapInfo, _Mapping]]] = ...) -> None: ...

class RobotMap(_message.Message):
    __slots__ = ["mapType", "mapExtInfo", "mapHead", "mapData", "mapInfo", "historyPose", "chargeStation", "currentPose", "virtualWalls", "areasInfo", "navigationPoints", "roomDataInfo", "roomMatrix", "roomChain", "objects", "furnitureInfo", "houseInfos"]
    MAPTYPE_FIELD_NUMBER: _ClassVar[int]
    MAPEXTINFO_FIELD_NUMBER: _ClassVar[int]
    MAPHEAD_FIELD_NUMBER: _ClassVar[int]
    MAPDATA_FIELD_NUMBER: _ClassVar[int]
    MAPINFO_FIELD_NUMBER: _ClassVar[int]
    HISTORYPOSE_FIELD_NUMBER: _ClassVar[int]
    CHARGESTATION_FIELD_NUMBER: _ClassVar[int]
    CURRENTPOSE_FIELD_NUMBER: _ClassVar[int]
    VIRTUALWALLS_FIELD_NUMBER: _ClassVar[int]
    AREASINFO_FIELD_NUMBER: _ClassVar[int]
    NAVIGATIONPOINTS_FIELD_NUMBER: _ClassVar[int]
    ROOMDATAINFO_FIELD_NUMBER: _ClassVar[int]
    ROOMMATRIX_FIELD_NUMBER: _ClassVar[int]
    ROOMCHAIN_FIELD_NUMBER: _ClassVar[int]
    OBJECTS_FIELD_NUMBER: _ClassVar[int]
    FURNITUREINFO_FIELD_NUMBER: _ClassVar[int]
    HOUSEINFOS_FIELD_NUMBER: _ClassVar[int]
    mapType: int
    mapExtInfo: MapExtInfo
    mapHead: MapHeadInfo
    mapData: MapDataInfo
    mapInfo: _containers.RepeatedCompositeFieldContainer[AllMapInfo]
    historyPose: DeviceHistoryPoseInfo
    chargeStation: DevicePoseDataInfo
    currentPose: DeviceCurrentPoseInfo
    virtualWalls: _containers.RepeatedCompositeFieldContainer[DeviceAreaDataInfo]
    areasInfo: _containers.RepeatedCompositeFieldContainer[DeviceAreaDataInfo]
    navigationPoints: _containers.RepeatedCompositeFieldContainer[DeviceNavigationPointDataInfo]
    roomDataInfo: _containers.RepeatedCompositeFieldContainer[RoomDataInfo]
    roomMatrix: DeviceRoomMatrix
    roomChain: _containers.RepeatedCompositeFieldContainer[DeviceRoomChainDataInfo]
    objects: _containers.RepeatedCompositeFieldContainer[ObjectDataInfo]
    furnitureInfo: _containers.RepeatedCompositeFieldContainer[FurnitureDataInfo]
    houseInfos: _containers.RepeatedCompositeFieldContainer[HouseInfo]
    def __init__(self, mapType: _Optional[int] = ..., mapExtInfo: _Optional[_Union[MapExtInfo, _Mapping]] = ..., mapHead: _Optional[_Union[MapHeadInfo, _Mapping]] = ..., mapData: _Optional[_Union[MapDataInfo, _Mapping]] = ..., mapInfo: _Optional[_Iterable[_Union[AllMapInfo, _Mapping]]] = ..., historyPose: _Optional[_Union[DeviceHistoryPoseInfo, _Mapping]] = ..., chargeStation: _Optional[_Union[DevicePoseDataInfo, _Mapping]] = ..., currentPose: _Optional[_Union[DeviceCurrentPoseInfo, _Mapping]] = ..., virtualWalls: _Optional[_Iterable[_Union[DeviceAreaDataInfo, _Mapping]]] = ..., areasInfo: _Optional[_Iterable[_Union[DeviceAreaDataInfo, _Mapping]]] = ..., navigationPoints: _Optional[_Iterable[_Union[DeviceNavigationPointDataInfo, _Mapping]]] = ..., roomDataInfo: _Optional[_Iterable[_Union[RoomDataInfo, _Mapping]]] = ..., roomMatrix: _Optional[_Union[DeviceRoomMatrix, _Mapping]] = ..., roomChain: _Optional[_Iterable[_Union[DeviceRoomChainDataInfo, _Mapping]]] = ..., objects: _Optional[_Iterable[_Union[ObjectDataInfo, _Mapping]]] = ..., furnitureInfo: _Optional[_Iterable[_Union[FurnitureDataInfo, _Mapping]]] = ..., houseInfos: _Optional[_Iterable[_Union[HouseInfo, _Mapping]]] = ...) -> None: ...
