import unittest
from helpers import mail

real_send = False
email = 'dm.chernyshov@gmail.com'


class MockMap:
    title = 'Map #hash123'
    hash = 'hash123'
    passkey = 'key321'


class TestSendEmail(unittest.TestCase):
    def setUp(self):
        pass

    def test_send_email(self):
        if real_send:
            m = MockMap()
            mail.send_email(email, m)
