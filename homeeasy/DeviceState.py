from datetime import time
from enum import IntEnum
from typing import List, Dict

from homeeasy import valueHelper


class Mode(IntEnum):
    Auto = 0
    Cool = 1
    Dry = 2
    Fan = 3
    Heat = 4


class FanSpeed(IntEnum):
    Auto = 0
    l1 = 1
    l2 = 2
    l3 = 3
    l4 = 4
    l5 = 5
    l6 = 6


class FanMode(IntEnum):
    Auto = 0
    l1 = 1
    l2 = 2
    l3 = 3
    l4 = 4
    l5 = 5
    l6 = 6
    Quite = 7
    Turbo = 8


class HorizontalFlowMode(IntEnum):
    Stop = 0
    Swing = 1
    Left = 2
    Left_Center = 3
    Center = 4
    Right_Center = 5
    Right = 6
    Left_Right = 12
    Swing_Wide = 13


class VerticalFlowMode(IntEnum):
    Stop = 0
    Swing = 1
    Top = 2
    Top_Center = 3
    Center = 4
    Bottom_Center = 5
    Bottom = 6


class TemperatureScale(IntEnum):
    Celsius = 0
    Fahrenheit = 1


# noinspection PyPep8Naming
class DeviceState:
    bits: List[bool]

    _wd_number_dict: Dict[str, int] = {'00000': 61, '10000': 61, '00001': 62, '10001': 63, '00010': 64, '10010': 65,
                                      '00011': 66, '10011': 67, '00100': 68, '10100': 68, '00101': 69, '10101': 70,
                                      '00110': 71, '10110': 72, '00111': 73, '10111': 74, '01000': 75, '11000': 76,
                                      '01001': 77, '11001': 77, '01010': 78, '11010': 79, '01011': 80, '11011': 81,
                                      '01100': 82, '11100': 83, '01101': 84, '11101': 85, '01110': 86, '11110': 86,
                                      '01111': 87, '11111': 88}
    _wd_number_dict_invert = {value: key for key, value in _wd_number_dict.items()}

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
            val_s = str(val).lower()
            val = False if val_s == 'false' or val_s == '0' else True
        self.bits[byte_pos * 8 + bit_pos] = bool(val)

    def _get_state_bits(self, x: int, y: int, count: int):
        val = 0
        for i in range(count):
            val = val << 1
            val += self._get_state_bit(x, y + i)
        return val

    def _set_state_bits(self, x: int, y: int, count: int, val: int):
        val = int(val)
        size = 8 * int((count / 8 + (1 if count % 8 > 0 else 0)))
        range_ = [self._get_bit(val, i, size) for i in range(size)]
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
        chunks = self._create_chunks(filtered, 6)

        chunks_with_values = [', '.join([f'{i}: {valueHelper.get_val(getattr(self, i))}' for i in j]) for j in chunks]
        out = ',\n'.join(chunks_with_values)
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
    def mode(self) -> Mode:
        return Mode(self._get_state_bits(3, 5, 3))

    @mode.setter
    def mode(self, value: Mode):
        if type(value) is str:
            s = str(value)
            try:
                value = Mode[s]
            except KeyError:
                value = Mode(int(s))
        self._set_state_bits(3, 5, 3, int(value))
            
    @property
    def power(self) -> bool:
        return self._get_state_bit(3, 4)

    @power.setter
    def power(self, value: bool):
        self._set_state_bit(3, 4, value)
            
    @property
    def fanSpeed(self) -> FanSpeed:
        return FanSpeed(self._get_state_bits(3, 1, 3))

    @fanSpeed.setter
    def fanSpeed(self, value: FanSpeed):
        if type(value) is str:
            s = str(value)
            try:
                value = FanSpeed[s]
            except KeyError:
                value = FanSpeed(int(s))
        self._set_state_bits(3, 1, 3, int(value))
            
    @property
    def turbo(self) -> bool:
        return self._get_state_bit(3, 0)

    @turbo.setter
    def turbo(self, value: bool):
        self._set_state_bit(3, 0, value)
    
    @property
    def quite(self) -> bool:
        return self._get_state_bit(4, 1)

    @quite.setter
    def quite(self, value: bool):
        self._set_state_bit(4, 1, value)
            
    @property
    def temperatureScale(self) -> TemperatureScale:
        return TemperatureScale(self._get_state_bit(4, 2))

    @temperatureScale.setter
    def temperatureScale(self, value: TemperatureScale):
        if type(value) is str:
            s = str(value)
            try:
                value = TemperatureScale[s]
            except KeyError:
                value = TemperatureScale(int(s))
        self._set_state_bit(4, 2, bool(value))
            
    @property
    def desiredTemperature(self) -> int:
        wen = self._get_state_bits(4, 3, 5)
        if not self.temperatureScale:
            wen = wen - 16 if wen >= 16 else wen
            wd_number = wen + 16 if wen > 0 else 16
        else:
            wen_str = format(wen, '#07b')[2:]
            wd_number = self._wd_number_dict[wen_str]
        return wd_number

    @desiredTemperature.setter
    def desiredTemperature(self, value: int):
        if not self.temperatureScale:
            val = value - 16 if value >= 16 else value
        else:
            val = self._wd_number_dict_invert[value];

        self._set_state_bits(4, 3, 5, val)
            
    @property
    def flowHorizontalMode(self) -> HorizontalFlowMode:
        return HorizontalFlowMode(self._get_state_bits(5, 0, 4))

    @flowHorizontalMode.setter
    def flowHorizontalMode(self, value: HorizontalFlowMode):
        if type(value) is str:
            s = str(value)
            try:
                value = HorizontalFlowMode[s]
            except KeyError:
                value = HorizontalFlowMode(int(s))
        self._set_state_bits(5, 0, 4, int(value))
            
    @property
    def flowVerticalMode(self) -> VerticalFlowMode:
        return VerticalFlowMode(self._get_state_bits(5, 4, 4))

    @flowVerticalMode.setter
    def flowVerticalMode(self, value: VerticalFlowMode):
        if type(value) is str:
            s = str(value)
            try:
                value = VerticalFlowMode[s]
            except KeyError:
                value = VerticalFlowMode(int(s))
        self._set_state_bits(5, 4, 4, int(value))
            
    @property
    def display(self) -> bool:
        return self._get_state_bit(6, 0)

    @display.setter
    def display(self, value: bool):
        self._set_state_bit(6, 0, value)
            
    @property
    def healthy(self) -> bool:
        return self._get_state_bit(6, 1)

    @healthy.setter
    def healthy(self, value: bool):
        self._set_state_bit(6, 1, value)
            
    @property
    def timingMode(self) -> bool:  # ?????
        return self._get_state_bit(6, 2)

    @timingMode.setter
    def timingMode(self, value: bool):
        self._set_state_bit(6, 2, value)
            
    @property
    def dryingMode(self) -> bool:  # Auxiliary heater (on, hot), Drying(off, cool or dry)
        return self._get_state_bit(6, 3)

    @dryingMode.setter
    def dryingMode(self, value: bool):
        self._set_state_bit(6, 3, value)
            
    @property
    def wdNumberMode(self) -> int:  # ??????
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
        value = self._str2time(value)
        val = value.hour * 60 + value.minute
        val_l = val & 0xff
        val_h = (val >> 8) & 0xff
        self._set_state_bits(7, 5, 3, val_h)
        self._set_state_bits(9, 0, 8, val_l)

    @staticmethod
    def _str2time(value):
        if type(value) is str:
            val_s = str(value)
            value = time.fromisoformat(val_s)
        return value

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
        value = self._str2time(value)
        val = value.hour * 60 + value.minute
        val_l = val & 0xff
        val_h = (val >> 8) & 0xff
        self._set_state_bits(7, 1, 3, val_h)
        self._set_state_bits(9, 0, 8, val_l)
            
    @property
    def wujiNum(self) -> int:  # ??????
        return self._get_state_bits(10, 0, 8)

    @wujiNum.setter
    def wujiNum(self, value: int):
        self._set_state_bits(10, 0, 8, value)
            
    @property
    def indoorTemperature(self) -> float:
        hi = self._get_state_bits(11, 0, 8)
        low = self._get_state_bits(12, 0, 8)
        return hi + 0.1 * low if not self.temperatureScale else hi * 1.3 + 32

    @property
    def fanMode(self) -> FanMode:
        wind_mode = int(self.fanSpeed)
        if self.turbo:
            wind_mode = 8
        else:
            if self.quite:
                wind_mode = 7
        return FanMode(wind_mode)

    @fanMode.setter
    def fanMode(self, value: FanMode):
        self.quite = False
        self.turbo = False

        if value == FanMode.Turbo:
            self.turbo = True
        elif value == FanMode.Quite:
            self.quite = True
        else:
            self.fanSpeed = FanSpeed(int(value))

    def __eq__(self, o: object) -> bool:
        return str(self) == str(o)
