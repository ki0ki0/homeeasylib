import unittest
from datetime import time
from unittest import TestCase
from homeeasy.DeviceState import DeviceState, Mode, FanSpeed


class TestDeviceState(TestCase):
    data = bytes([170, 170, 18, 0, 10, 10, 0, 12, 7, 0, 196, 0, 0, 0, 0, 22, 5, 0, 0, 0, 108])

    # {"runMode": "100", "boot": 1, "windLevel": "000", "cpmode": 0, "mute": 0, "temtyp": 0, "wdNumber": 23,
    #  "windLR": "0000", "windTB": "0000", "lighting": 1, "healthy": 1, "timingMode": 0, "dryingmode": 0,
    #  "wdNumberMode": "01", "sleep": 0, "eco": 0, "bootEnabled": 0, "bootTime": "00:00", "shutEnabled": 0,
    #  "shutTime": "00:00", "wujiNum": 0, "indoorTemperature": "22.5", "windMode": 0}

    def test_run_mode(self):
        self.assertEqual(Mode.Heat, DeviceState(self.data).mode)

    def test_run_mode_set(self):
        state = DeviceState(self.data)
        state.mode = Mode.Fan
        self.assertEqual(Mode.Fan, state.mode)

    def test_boot(self):
        self.assertEqual(True, DeviceState(self.data).power)

    def test_boot_set(self):
        state = DeviceState(self.data)
        state.power = False
        self.assertEqual(False, state.power)

    def test_wind_level(self):
        self.assertEqual(FanSpeed.Auto, DeviceState(self.data).fanSpeed)

    def test_wind_level_set(self):
        state = DeviceState(self.data)
        state.fanSpeed = FanSpeed.l5
        self.assertEqual(FanSpeed.l5, state.fanSpeed)

    def test_cpmode(self):
        self.assertEqual(False, DeviceState(self.data).turbo)

    def test_cpmode_set(self):
        state = DeviceState(self.data)
        state.turbo = True
        self.assertEqual(True, state.turbo)

    def test_mute(self):
        self.assertEqual(False, DeviceState(self.data).quite)

    def test_mute_set(self):
        state = DeviceState(self.data)
        state.quite = True
        self.assertEqual(True, state.power)

    def test_temtyp(self):
        self.assertEqual(0, DeviceState(self.data).temperatureScale)

    def test_temtyp_set(self):
        state = DeviceState(self.data)
        state.temperatureScale = True
        self.assertEqual(True, state.temperatureScale)

    def test_wdNumber(self):
        self.assertEqual(23, DeviceState(self.data).desiredTemperature)

    def test_wdNumber_set(self):
        state = DeviceState(self.data)
        state.desiredTemperature = 17
        self.assertEqual(17, state.desiredTemperature)

    def test_windLR(self):
        self.assertEqual(0, DeviceState(self.data).flowHorizontalMode)

    def test_windLR_set(self):
        state = DeviceState(self.data)
        state.flowHorizontalMode = 3
        self.assertEqual(3, state.flowHorizontalMode)

    def test_windTB(self):
        self.assertEqual(0, DeviceState(self.data).flowVerticalMode)

    def test_windTB_set(self):
        state = DeviceState(self.data)
        state.flowVerticalMode = 3
        self.assertEqual(3, state.flowVerticalMode)

    def test_lighting(self):
        self.assertEqual(True, DeviceState(self.data).display)

    def test_lighting_set(self):
        state = DeviceState(self.data)
        state.display = False
        self.assertEqual(False, state.display)

    def test_healthy(self):
        self.assertEqual(True, DeviceState(self.data).healthy)

    def test_healthy_set(self):
        state = DeviceState(self.data)
        state.healthy = False
        self.assertEqual(False, state.healthy)

    def test_timingMode(self):
        self.assertEqual(0, DeviceState(self.data).timingMode)

    def test_timingMode_set(self):
        state = DeviceState(self.data)
        state.timingMode = True
        self.assertEqual(True, state.timingMode)

    def test_dryingmode(self):
        self.assertEqual(False, DeviceState(self.data).dryingMode)

    def test_dryingmode_set(self):
        state = DeviceState(self.data)
        state.dryingMode = True
        self.assertEqual(True, state.dryingMode)

    def test_wdNumberMode(self):
        self.assertEqual(1, DeviceState(self.data).wdNumberMode)

    def test_wdNumberMode_set(self):
        state = DeviceState(self.data)
        state.wdNumberMode = 3
        self.assertEqual(3, state.wdNumberMode)

    def test_sleep(self):
        self.assertEqual(False, DeviceState(self.data).sleep)

    def test_sleep_set(self):
        state = DeviceState(self.data)
        state.sleep = True
        self.assertEqual(True, state.sleep)

    def test_eco(self):
        self.assertEqual(False, DeviceState(self.data).eco)

    def test_eco_set(self):
        state = DeviceState(self.data)
        state.eco = True
        self.assertEqual(True, state.eco)

    def test_bootEnabled(self):
        self.assertEqual(False, DeviceState(self.data).bootEnabled)

    def test_bootEnabled_set(self):
        state = DeviceState(self.data)
        state.bootEnabled = True
        self.assertEqual(True, state.bootEnabled)

    def test_bootTime(self):
        self.assertEqual(time(0, 0), DeviceState(self.data).bootTime)

    def test_bootTime_set(self):
        state = DeviceState(self.data)
        state.bootTime = time(10, 12)
        self.assertEqual(time(10, 12), state.bootTime)

    def test_shutEnabled(self):
        self.assertEqual(False, DeviceState(self.data).shutEnabled)

    def test_shutEnabled_set(self):
        state = DeviceState(self.data)
        state.shutEnabled = True
        self.assertEqual(True, state.shutEnabled)

    def test_shutTime(self):
        self.assertEqual(time(0, 0), DeviceState(self.data).shutTime)

    def test_shutTime_set(self):
        state = DeviceState(self.data)
        state.shutTime = time(17, 18)
        self.assertEqual(time(17, 18), state.shutTime)

    def test_wujiNum(self):
        self.assertEqual(0, DeviceState(self.data).wujiNum)

    def test_wujiNum_set(self):
        state = DeviceState(self.data)
        state.wujiNum = 3
        self.assertEqual(3, state.wujiNum)

    def test_indoorTemperature(self):
        self.assertEqual(22.5, DeviceState(self.data).indoorTemperature)

    def test_windMode(self):
        self.assertEqual(0, DeviceState(self.data).fanMode)

    def test_windMode_set(self):
        state = DeviceState(self.data)
        state.fanMode = 7
        self.assertEqual(7, state.fanMode)

    def test_cmd(self):
        expected = b'\xaa\xaa\x12\x01\n\n\x00\x0c\x07\x00\xc4\x00\x00\x00\x00\x16\x05\x00\x00\x00m'
        self.assertEqual(expected, DeviceState(self.data).cmd)

    @unittest.skip("debug only")
    def test_str(self):
        s = str(DeviceState(self.data))
        self.assertEqual('', s)

    def test_mode_quite_set(self):
        state = DeviceState(self.data)
        state.mode = Mode.Fan
        state.quite = True
        self.assertEqual(Mode.Fan, state.mode)
        self.assertEqual(True, state.quite)
