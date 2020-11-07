from datetime import time
from enum import IntEnum
from typing import List


class RunMode(IntEnum):
    Auto = 0
    Cool = 1
    Dry = 2
    Wind = 3
    Hot = 4


class WindLevel(IntEnum):
    Auto = 0  # Auto
    l1 = 1
    l2 = 2
    l3 = 3
    l4 = 4
    l5 = 5
    l6 = 6


class WindMode(IntEnum):
    Auto = 0  # Auto
    l1 = 1
    l2 = 2
    l3 = 3
    l4 = 4
    l5 = 5
    l6 = 6
    Quite = 7
    Turbo = 8  # Turbo


class WindLRMode(IntEnum):
    Stop = 0
    Cycle = 1
    Left = 2
    Left_Center = 3
    Center = 4
    Right_Center = 5
    Right = 6
    Left_Right = 12
    Cycle_Symmetrically = 13


class WindTBMode(IntEnum):
    Stop = 0
    Cycle = 1
    Top = 2
    l3 = 3
    Center = 4
    l5 = 5
    Bottom = 6


# noinspection PyPep8Naming
class DeviceState:
    bits: List[bool]

    def __init__(self, message: bytes) -> None:
        self.raw = message

    @staticmethod
    def _get_bit(x: int, b: int, size: int = 8) -> bool:
        return bool((x >> (size-1 - b)) & 1)

    def _bytes2bits(self, x: bytes) -> List[bool]:
        return [self._get_bit(x[int(pos / 8)], pos % 8) for pos in range(len(x) * 8)]

    @staticmethod
    def _bits2byte(bit0: bool, bit1: bool, bit2: bool, bit3: bool, bit4: bool, bit5: bool, bit6: bool, bit7: bool):
        byte_ = bit7 + (bit6 << 1) + (bit5 << 2) + (bit4 << 3) + (bit3 << 4) + (bit2 << 5) + (bit1 << 6) + (bit0 << 7)
        return byte_

    def _bits2bytes(self) -> bytes:
        bits = self.bits
        bytes_count = int(len(bits) / 8)
        list_ = [self._bits2byte(bits[pos * 8 + 0], bits[pos * 8 + 1], bits[pos * 8 + 2], bits[pos * 8 + 3],
                                 bits[pos * 8 + 4], bits[pos * 8 + 5], bits[pos * 8 + 6], bits[pos * 8 + 7]) for pos in
                 range(bytes_count)]
        return bytes(list_)

    def _get_state_bit(self, x: int, y: int) -> bool:
        x1 = x + 4
        return self.bits[x1 * 8 + y]

    def _set_state_bit(self, byte_pos: int, bit_pos: int, val: bool):
        byte_pos = byte_pos + 4  # offset on header size
        if type(val) is str:
            val = False if val == 'False' or val == 'false' else True
        self.bits[byte_pos * 8 + bit_pos] = bool(val)

    def _get_state_bits(self, x: int, y: int, count: int):
        val = 0
        for i in range(count):
            val = val << 1
            val += self._get_state_bit(x, y + i)
        return val

    def _set_state_bits(self, x: int, y: int, count: int, val: int):
        ival = int(val)
        size = 8 * int((count / 8 + (1 if count % 8 > 0 else 0)))
        range_ = [self._get_bit(ival, i, size) for i in range(size)]
        bits = range_[-count:]

        for i in range(count):
            self._set_state_bit(x, y + i, bool(bits[i]))

    # noinspection PyMethodMayBeStatic
    def _create_chunks(self, list_name, n):
        for i in range(0, len(list_name), n):
            yield list_name[i:i + n]

    def __repr__(self):
        keys = [i for i in dir(self) if not i.startswith('_')]
        skip = ['bits', 'cmd', 'raw']
        filtered = [key for key in keys if key not in skip]
        chunks = self._create_chunks(filtered, 7)

        in_filtered = [', '.join([f'{i}: {getattr(self, i)}' for i in j]) for j in chunks]
        out = ',\n'.join(in_filtered)
        return out

    def __str__(self):
        return self.__repr__()

    @property
    def raw(self) -> bytes:
        return self._bits2bytes()

    @raw.setter
    def raw(self, value: bytes):
        self.bits = self._bytes2bits(value[:21])

    @property
    def cmd(self) -> bytes:
        bits_bytes = bytearray(self._bits2bytes())
        bits_bytes[3] = 0x01
        code = 0x00
        for i in bits_bytes[:-1]:
            code += i
        bits_bytes[-1] = code & 0xFF
        return bytes(bits_bytes)

    @property
    def runMode(self) -> RunMode:
        return RunMode(self._get_state_bits(3, 5, 3))

    @runMode.setter
    def runMode(self, value: RunMode):
        self._set_state_bits(3, 5, 3, int(value))
            
    @property
    def boot(self) -> bool:
        return self._get_state_bit(3, 4)

    @boot.setter
    def boot(self, value: bool):
        self._set_state_bit(3, 4, value)
            
    @property
    def windLevel(self) -> WindLevel:
        return WindLevel(self._get_state_bits(3, 1, 3))

    @windLevel.setter
    def windLevel(self, value: WindLevel):
        self._set_state_bits(3, 1, 3, int(value))
            
    @property
    def cpmode(self) -> bool:  # Turbo
        return self._get_state_bit(3, 0)

    @cpmode.setter
    def cpmode(self, value: bool):
        self._set_state_bit(3, 0, value)
    
    @property
    def mute(self) -> bool:
        return self._get_state_bit(4, 1)

    @mute.setter
    def mute(self, value: bool):
        self._set_state_bit(4, 1, value)
            
    @property
    def temtyp(self) -> bool:
        return self._get_state_bit(4, 2)

    @temtyp.setter
    def temtyp(self, value: bool):
        self._set_state_bit(4, 2, value)
            
    @property
    def wdNumber(self) -> int:  # target temperature
        wen = self._get_state_bits(4, 3, 5)
        wen = wen - 16 if wen >= 16 else wen
        wd_number = wen + 16 if wen > 0 else 16
        return wd_number

    @wdNumber.setter
    def wdNumber(self, value: int):
        pass
            
    @property
    def windLR(self) -> int:
        return self._get_state_bits(5, 0, 4)

    @windLR.setter
    def windLR(self, value: int):
        self._set_state_bits(5, 0, 4, value)
            
    @property
    def windTB(self) -> int:
        return self._get_state_bits(5, 4, 4)

    @windTB.setter
    def windTB(self, value: int):
        self._set_state_bits(5, 4, 4, value)
            
    @property
    def lighting(self) -> bool:
        return self._get_state_bit(6, 0)

    @lighting.setter
    def lighting(self, value: bool):
        self._set_state_bit(6, 0, value)
            
    @property
    def healthy(self) -> bool:
        return self._get_state_bit(6, 1)

    @healthy.setter
    def healthy(self, value: bool):
        self._set_state_bit(6, 1, value)
            
    @property
    def timingMode(self) -> bool:
        return self._get_state_bit(6, 2)

    @timingMode.setter
    def timingMode(self, value: bool):
        self._set_state_bit(6, 2, value)
            
    @property
    def dryingmode(self) -> bool:  # Auxiliary heater (on, hot), Drying(off, cool or dry)
        return self._get_state_bit(6, 3)

    @dryingmode.setter
    def dryingmode(self, value: bool):
        self._set_state_bit(6, 3, value)
            
    @property
    def wdNumberMode(self) -> int:
        return self._get_state_bits(6, 4, 2)

    @wdNumberMode.setter
    def wdNumberMode(self, value: int):
        self._set_state_bits(6, 4, 2, value)
            
    @property
    def sleep(self) -> bool:
        return self._get_state_bit(6, 6)

    @sleep.setter
    def sleep(self, value: bool):
        self._set_state_bit(6, 6, value)
            
    @property
    def eco(self) -> bool:
        return self._get_state_bit(6, 7)

    @eco.setter
    def eco(self, value: bool):
        self._set_state_bit(6, 7, value)
            
    @property
    def bootEnabled(self) -> bool:
        return self._get_state_bit(7, 4)

    @bootEnabled.setter
    def bootEnabled(self, value: bool):
        self._set_state_bit(7, 4, value)
            
    @property
    def bootTime(self) -> time:
        val_h = self._get_state_bits(7, 5, 3)
        val_l = self._get_state_bits(9, 0, 8)
        val = (val_h << 8) + val_l
        v_hour = int(val / 60)
        v_min = int(val % 60)
        return time(v_hour, v_min)

    @bootTime.setter
    def bootTime(self, value: time):
        if type(value) is str:
            value = time.fromisoformat(value)
        val = value.hour * 60 + value.minute
        val_l = val & 0xff
        val_h = (val >> 8) & 0xff
        self._set_state_bits(7, 5, 3, val_h)
        self._set_state_bits(9, 0, 8, val_l)
            
    @property
    def shutEnabled(self) -> bool:
        return self._get_state_bit(7, 0)

    @shutEnabled.setter
    def shutEnabled(self, value: bool):
        self._set_state_bit(7, 0, value)
            
    @property
    def shutTime(self) -> time:
        val_h = self._get_state_bits(7, 1, 3)
        val_l = self._get_state_bits(9, 0, 8)
        val = (val_h << 8) + val_l
        v_hour = int(val / 60)
        v_min = int(val % 60)
        return time(v_hour, v_min)

    @shutTime.setter
    def shutTime(self, value: time):
        if type(value) is str:
            value = time.fromisoformat(value)
        val = value.hour * 60 + value.minute
        val_l = val & 0xff
        val_h = (val >> 8) & 0xff
        self._set_state_bits(7, 1, 3, val_h)
        self._set_state_bits(9, 0, 8, val_l)
            
    @property
    def wujiNum(self) -> int:
        return self._get_state_bits(10, 0, 8)

    @wujiNum.setter
    def wujiNum(self, value: int):
        self._set_state_bits(10, 0, 8, value)
            
    @property
    def indoorTemperature(self) -> float:
        hi = self._get_state_bits(11, 0, 8)
        low = self._get_state_bits(12, 0, 8)
        return hi + 0.1 * low if not self.temtyp else hi * 1.3 + 32

    @property
    def windMode(self) -> WindMode:
        wind_mode = int(self.windLevel)
        if self.cpmode:
            wind_mode = 8
        else:
            if self.mute:
                wind_mode = 7
        return WindMode(wind_mode)

    @windMode.setter
    def windMode(self, value: WindMode):
        pass
