import unittest

from lib.utils import doEmailLog

class EmailLogTest(unittest.TestCase):

    def test_send(self):
        config = {
            'from_addr':'***',
            'pass':'***',
            'to_addr':'***',
            'smtp_server':'***'
        }
        doEmailLog(config)