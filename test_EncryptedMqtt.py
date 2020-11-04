from unittest import TestCase

from EncryptedMqtt import EncryptedMqtt


class TestEncryptedMqtt(TestCase):
    def test_get_key_1(self):
        self.assertEqual('a3d44c718acaead0', EncryptedMqtt.get_key('09ba20043c42').decode("utf-8"))

    def test_get_key_2(self):
        self.assertEqual('6e96059eb05bbf76', EncryptedMqtt.get_key('08bc270447e3').decode("utf-8"))

    def test_decrypt(self):
        key = bytes.fromhex("33323931356565303561643566623034")  # mac ('08bc20043d34')
        encrypted = bytes.fromhex('4b69753535d25af38a1ed107312a6c742da7506064d6c4c14c7a210d8888ed47')
        decrypted = EncryptedMqtt.decrypt(encrypted, key)
        expected = bytes.fromhex("d2f15e050abd3fc7f07e753257485c5e05000000b2")
        self.assertEqual(expected, decrypted)
