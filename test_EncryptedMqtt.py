from unittest import TestCase
import EncryptedMqtt


class EncryptedMqttTests(TestCase):
    def test_get_key_1(self):
        self.assertEqual('a3d44c718acaead0', EncryptedMqtt.get_key('09ba20043c42'))

    def test_get_key_2(self):
        self.assertEqual('6e96059eb05bbf76', EncryptedMqtt.get_key('08bc270447e3'))
