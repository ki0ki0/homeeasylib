from dataclasses import dataclass
from datetime import time
from enum import Enum


class RunMode(Enum):
    Auto = 0
    Cool = 1
    Chushi = 2
    Wind = 3
    Hot = 4


class WindLevel(Enum):
    l0 = 0
    l1 = 1
    l2 = 2
    l3 = 3
    l4 = 4
    l5 = 5
    l6 = 6


class WindMode(Enum):
    l0 = 0
    l1 = 1
    l2 = 2
    l3 = 3
    l4 = 4
    l5 = 5
    l6 = 6
    Cp = 7
    Mute = 8


@dataclass
class DeviceState:
    runMode: RunMode
    boot: bool
    windLevel: WindLevel
    # cpmode: int
    # mute: int
    # temtyp: int
    # wdNumber: int
    windLR: int
    windTB: int
    lighting: bool
    healthy: bool
    # timingMode: int
    # dryingmode: int
    # wdNumberMode: str
    sleep: bool
    eco: bool
    bootEnabled: bool
    bootTime: time
    shutEnabled: bool
    shutTime: time
    # wujiNum: str
    indoorTemperature: float
    windMode: WindMode