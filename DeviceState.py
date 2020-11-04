class DeviceState:
    array_2 = {'00000': 61, '10000': 61, '00001': 62, '10001': 63, '00010': 64, '10010': 65, '00011': 66, '10011': 67,
               '00100': 68, '10100': 68, '00101': 69, '10101': 70, '00110': 71, '10110': 72, '00111': 73, '10111': 74,
               '01000': 75, '11000': 76, '01001': 77, '11001': 77, '01010': 78, '11010': 79, '01011': 80, '11011': 81,
               '01100': 82, '11100': 83, '01101': 84, '11101': 85, '01110': 86, '11110': 86, '01111': 87, '11111': 88};

    @staticmethod
    def int2bits(x):
        return [int(digit) for digit in bin(x)[2:].zfill(8)]

    def parse3(self, byte):
        bit = self.int2bits(byte)
        run_mode = "".join(map(str, [bit[5], bit[6], bit[7]]))
        boot = bit[4]
        wind_level = "".join(map(str, [bit[1], bit[2], bit[3]]))
        cpmode = bit[0]
        return {
            "runMode": run_mode,
            "boot": boot,
            "windLevel": wind_level,
            "cpmode": cpmode
        }

    def parse4(self, byte):
        bit = self.int2bits(byte)
        mute = bit[1]
        mode = bit[2]
        wen_two = "".join(map(str, [bit[3], bit[4], bit[5], bit[6], bit[7]]))

        if mode == 0:
            wen = int(wen_two, 2)
            wen = wen - 16 if wen >= 16 else wen
            wd_number = wen + 16 if wen > 0 else 16
        else:
            wd_number = self.array_2[wen_two]

        return {
            "mute": mute,
            "temtyp": mode,
            "wdNumber": wd_number
        }

    def parse5(self, byte):
        bits = self.int2bits(byte)

        windLR = "".join(map(str, [bits[0], bits[1], bits[2], bits[3]]))
        windTB = "".join(map(str, [bits[4], bits[5], bits[6], bits[7]]))
        return {
            "windLR": windLR,
            "windTB": windTB
        }

    def parse6(self, byte):
        bits = self.int2bits(byte)
        return {
            "lighting": bits[0],
            "healthy": bits[1],
            "timingMode": bits[2],
            "dryingmode": bits[3],
            "wdNumberMode": str(bits[4]) + str(bits[5]),
            "sleep": bits[6],
            "eco": bits[7]
        }

    def parse789(self, byte7, byte8, byte9):
        bits7 = self.int2bits(byte7)
        bits8 = self.int2bits(byte8)
        bits9 = self.int2bits(byte9)
        shut_e = bits7[0]
        shut_t = "".join(map(str, [bits7[1], bits7[2], bits7[3]] + bits9))
        boot_e = bits7[4]
        boot_t = "".join(map(str, [bits7[5], bits7[6], bits7[7]] + bits8))
        boot = int(boot_t, 2)
        shut = int(shut_t, 2)
        boot_hor = int(boot / 60)
        boot_min = int(boot % 60)
        shut_hor = int(shut / 60)
        shut_min = int(shut % 60)
        boot_time = str(boot_hor).zfill(2) + ":" + str(boot_min).zfill(2)
        shut_time = str(shut_hor).zfill(2) + ":" + str(shut_min).zfill(2)
        return {
            "bootEnabled": boot_e,
            "bootTime": boot_time,
            "shutEnabled": shut_e,
            "shutTime": shut_time
        }

    def parse10(self, byte10):
        return {
            "wujiNum": byte10
        }

    def parse11_12(self, temtyp, byte11, byte12):
        temp = byte11 + 0.1 * byte12 if temtyp == 0 else byte11 * 1.8 + 32
        return {
            "indoorTemperature": str(temp)
        }

    def parse(self, message):
        data3 = self.parse3(message[4 + 3])
        data4 = self.parse4(message[4 + 4])
        data5 = self.parse5(message[4 + 5])
        data6 = self.parse6(message[4 + 6])
        data789 = self.parse789(message[4 + 7], message[4 + 8], message[4 + 9])
        data10 = self.parse10(message[4 + 10])
        data11_12 = self.parse11_12(data4["temtyp"], message[4 + 11], message[4 + 12])
        cpmode = data3["cpmode"]
        mute = data4["mute"]
        wind_mode = int(data3["windLevel"], 2)
        if cpmode:
            wind_mode = 8
        else:
            if mute:
                wind_mode = 7

        return {**data3, **data4, **data5, **data6, **data789, **data10, **data11_12, **{"windMode": wind_mode}}
