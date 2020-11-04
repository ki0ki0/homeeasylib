from unittest import TestCase
from DeviceState import DeviceState


class TestDeviceState(TestCase):
    def test_int2bit_1(self):
        state = DeviceState()
        self.assertEqual([0, 0, 0, 0, 0, 0, 0, 1], state.int2bits(1))

    def test_int2bit_16(self):
        state = DeviceState()
        self.assertEqual([0, 0, 0, 1, 0, 0, 0, 0], state.int2bits(16))

    def test_int2bit_170(self):
        state = DeviceState()
        self.assertEqual([1, 0, 1, 0, 1, 0, 1, 0], state.int2bits(170))

    def test_parse_1(self):
        state = DeviceState()
        enc = bytes([170, 170, 18, 1, 10, 10, 0, 12, 7, 0, 196, 0, 0, 0, 0, 22, 5, 0, 0, 0, 109])
        dec = {"runMode": "100", "boot": 1, "windLevel": "000", "cpmode": 0, "mute": 0, "temtyp": 0, "wdNumber": 23,
               "windLR": "0000", "windTB": "0000", "lighting": 1, "healthy": 1, "timingMode": 0, "dryingmode": 0,
               "wdNumberMode": "01", "sleep": 0, "eco": 0, "bootEnabled": 0, "bootTime": "00:00", "shutEnabled": 0,
               "shutTime": "00:00", "wujiNum": 0, "indoorTemperature": "22.5", "windMode": 0}
        self.assertEqual(dec, state.parse(enc))

    def test_parse_2(self):
        state = DeviceState()
        enc = bytes([170, 170, 18, 0, 10, 10, 0, 4, 6, 0, 196, 0, 0, 0, 60, 22, 0, 0, 0, 0, 154])
        dec = {"runMode": "100", "boot": 0, "windLevel": "000", "cpmode": 0, "mute": 0, "temtyp": 0, "wdNumber": 22,
               "windLR": "0000", "windTB": "0000", "lighting": 1, "healthy": 1, "timingMode": 0, "dryingmode": 0,
               "wdNumberMode": "01", "sleep": 0, "eco": 0, "bootEnabled": 0, "bootTime": "00:00", "shutEnabled": 0,
               "shutTime": "00:00", "wujiNum": 60, "indoorTemperature": "22.0", "windMode": 0}
        self.assertEqual(dec, state.parse(enc))
