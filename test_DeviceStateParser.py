from datetime import time
from unittest import TestCase

from DeviceState import DeviceState, RunMode, WindLevel, WindMode
from DeviceStateParser import DeviceStateParser


class TestDeviceStateParser(TestCase):
    def test_int2bit_1(self):
        state = DeviceStateParser()
        self.assertEqual([0, 0, 0, 0, 0, 0, 0, 1], state.int2bits(1))

    def test_int2bit_16(self):
        state = DeviceStateParser()
        self.assertEqual([0, 0, 0, 1, 0, 0, 0, 0], state.int2bits(16))

    def test_int2bit_170(self):
        state = DeviceStateParser()
        self.assertEqual([1, 0, 1, 0, 1, 0, 1, 0], state.int2bits(170))

    def test_parse2dict_1(self):
        state = DeviceStateParser()
        enc = bytes([170, 170, 18, 1, 10, 10, 0, 12, 7, 0, 196, 0, 0, 0, 0, 22, 5, 0, 0, 0, 109])
        dec = {"runMode": "100", "boot": 1, "windLevel": "000", "cpmode": 0, "mute": 0, "temtyp": 0, "wdNumber": 23,
               "windLR": "0000", "windTB": "0000", "lighting": 1, "healthy": 1, "timingMode": 0, "dryingmode": 0,
               "wdNumberMode": "01", "sleep": 0, "eco": 0, "bootEnabled": 0, "bootTime": "00:00", "shutEnabled": 0,
               "shutTime": "00:00", "wujiNum": 0, "indoorTemperature": "22.5", "windMode": 0}
        self.assertEqual(dec, state.parse2dict(enc))

    def test_parse2dict_2(self):
        state = DeviceStateParser()
        enc = bytes([170, 170, 18, 0, 10, 10, 0, 4, 6, 0, 196, 0, 0, 0, 60, 22, 0, 0, 0, 0, 154])
        dec = {"runMode": "100", "boot": 0, "windLevel": "000", "cpmode": 0, "mute": 0, "temtyp": 0, "wdNumber": 22,
               "windLR": "0000", "windTB": "0000", "lighting": 1, "healthy": 1, "timingMode": 0, "dryingmode": 0,
               "wdNumberMode": "01", "sleep": 0, "eco": 0, "bootEnabled": 0, "bootTime": "00:00", "shutEnabled": 0,
               "shutTime": "00:00", "wujiNum": 60, "indoorTemperature": "22.0", "windMode": 0}
        self.assertEqual(dec, state.parse2dict(enc))

    def test_parse2dict_3(self):
        state = DeviceStateParser()
        enc = bytes([170, 170, 18, 0, 10, 10, 0, 12, 7, 0, 196, 0, 0, 0, 0, 22, 5, 0, 0, 0, 108])
        dec = {"runMode": "100", "boot": 1, "windLevel": "000", "cpmode": 0, "mute": 0, "temtyp": 0, "wdNumber": 23,
               "windLR": "0000", "windTB": "0000", "lighting": 1, "healthy": 1, "timingMode": 0, "dryingmode": 0,
               "wdNumberMode": "01", "sleep": 0, "eco": 0, "bootEnabled": 0, "bootTime": "00:00", "shutEnabled": 0,
               "shutTime": "00:00", "wujiNum": 0, "indoorTemperature": "22.5", "windMode": 0}
        self.assertEqual(dec, state.parse2dict(enc))

    def test_parse_1(self):
        parser = DeviceStateParser()
        enc = bytes([170, 170, 18, 0, 10, 10, 0, 4, 6, 0, 196, 0, 0, 0, 60, 22, 0, 0, 0, 0, 154])
        state = DeviceState(RunMode.Hot, False, WindLevel.l0, False, False, False, 22, 0, 0, True, True, True, False, 1,
                            False, False, False, time(0, 0), False, time(0, 0), 60, 22.0, WindMode.l0)
        parse = parser.parse(enc)
        self.assertEqual(state, parse)
