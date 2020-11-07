import unittest
from datetime import time
from unittest import TestCase

from DeviceState import DeviceState, RunMode, WindLevel


class TestDeviceState(TestCase):
    data = bytes([170, 170, 18, 0, 10, 10, 0, 12, 7, 0, 196, 0, 0, 0, 0, 22, 5, 0, 0, 0, 108])

    # {"runMode": "100", "boot": 1, "windLevel": "000", "cpmode": 0, "mute": 0, "temtyp": 0, "wdNumber": 23,
    #  "windLR": "0000", "windTB": "0000", "lighting": 1, "healthy": 1, "timingMode": 0, "dryingmode": 0,
    #  "wdNumberMode": "01", "sleep": 0, "eco": 0, "bootEnabled": 0, "bootTime": "00:00", "shutEnabled": 0,
    #  "shutTime": "00:00", "wujiNum": 0, "indoorTemperature": "22.5", "windMode": 0}

    def test_run_mode(self):
        self.assertEqual(RunMode.Hot, DeviceState(self.data).runMode)

    def test_run_mode_set(self):
        state = DeviceState(self.data)
        state.runMode = RunMode.Wind
        self.assertEqual(RunMode.Wind, state.runMode)

    def test_boot(self):
        self.assertEqual(True, DeviceState(self.data).boot)

    def test_boot_set(self):
        state = DeviceState(self.data)
        state.boot = False
        self.assertEqual(False, state.boot)

    def test_wind_level(self):
        self.assertEqual(WindLevel.Auto, DeviceState(self.data).windLevel)

    def test_wind_level_set(self):
        state = DeviceState(self.data)
        state.windLevel = WindLevel.l5
        self.assertEqual(WindLevel.l5, state.windLevel)

    def test_cpmode(self):
        self.assertEqual(False, DeviceState(self.data).cpmode)

    def test_cpmode_set(self):
        state = DeviceState(self.data)
        state.cpmode = True
        self.assertEqual(True, state.cpmode)

    def test_mute(self):
        self.assertEqual(False, DeviceState(self.data).mute)

    def test_mute_set(self):
        state = DeviceState(self.data)
        state.mute = True
        self.assertEqual(True, state.boot)

    def test_temtyp(self):
        self.assertEqual(0, DeviceState(self.data).temtyp)

    def test_temtyp_set(self):
        state = DeviceState(self.data)
        state.temtyp = True
        self.assertEqual(True, state.temtyp)

    def test_wdNumber(self):
        self.assertEqual(23, DeviceState(self.data).wdNumber)

    @unittest.skip("not implemented yet")
    def test_wdNumber_set(self):
        state = DeviceState(self.data)
        state.wdNumber = 17
        self.assertEqual(17, state.wdNumber)

    def test_windLR(self):
        self.assertEqual(0, DeviceState(self.data).windLR)

    def test_windLR_set(self):
        state = DeviceState(self.data)
        state.windLR = 3
        self.assertEqual(3, state.windLR)

    def test_windTB(self):
        self.assertEqual(0, DeviceState(self.data).windTB)

    def test_windTB_set(self):
        state = DeviceState(self.data)
        state.windTB = 3
        self.assertEqual(3, state.windTB)

    def test_lighting(self):
        self.assertEqual(True, DeviceState(self.data).lighting)

    def test_lighting_set(self):
        state = DeviceState(self.data)
        state.lighting = False
        self.assertEqual(False, state.lighting)

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
        self.assertEqual(False, DeviceState(self.data).dryingmode)

    def test_dryingmode_set(self):
        state = DeviceState(self.data)
        state.dryingmode = True
        self.assertEqual(True, state.dryingmode)

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
        self.assertEqual(0, DeviceState(self.data).windMode)

    @unittest.skip("not implemented yet")
    def test_windMode_set(self):
        state = DeviceState(self.data)
        state.windMode = 7
        self.assertEqual(7, state.windMode)

    def test_cmd(self):
        expeted = b'\xaa\xaa\x12\x01\n\n\x00\x0c\x07\x00\xc4\x00\x00\x00\x00\x16\x05\x00\x00\x00m'
        self.assertEqual(expeted, DeviceState(self.data).cmd)
