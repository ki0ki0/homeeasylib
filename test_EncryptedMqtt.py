from unittest import TestCase

from Crypto.Cipher import AES

from EncryptedMqtt import EncryptedMqtt


class TestEncryptedMqtt(TestCase):
    def test_get_key_1(self):
        self.assertEqual('a3d44c718acaead0', EncryptedMqtt.get_key('09ba20043c42').decode("utf-8"))

    def test_get_key_2(self):
        self.assertEqual('6e96059eb05bbf76', EncryptedMqtt.get_key('08bc270447e3').decode("utf-8"))

    def test_encrypt1(self):
        key = "a3d44c718acaead0".encode('utf-8')
        expected = '2776bf014dae8a1651994552b19e29969870167b550749d2362953a167fcc778'
        raw = bytes([170, 170, 18, 160, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26])
        mqtt = EncryptedMqtt()
        encrypt = mqtt.encrypt(raw, key)
        encrypted = encrypt.hex()
        self.assertEqual(expected, encrypted)

    def test_decrypt(self):
        key = "a3d44c718acaead0".encode('utf-8')
        encrypted = bytes.fromhex('2776bf014dae8a1651994552b19e29969870167b550749d2362953a167fcc778')
        mqtt = EncryptedMqtt()
        decrypted = mqtt.decrypt(encrypted, key)
        expected = bytes([170, 170, 18, 160, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26])
        self.assertEqual(expected, decrypted)

