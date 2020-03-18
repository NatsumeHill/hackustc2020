import unittest

from lib.utils import doEmailLog, loadConfigFile, doSMSLog

class EmailLogTest(unittest.TestCase):

    def test_send(self):
        config = {
            'from_addr':'***',
            'pass':'***',
            'to_addr':'***',
            'smtp_server':'***'
        }
        doEmailLog(config)

class LoadConfigTest(unittest.TestCase):
    
    def test_load(self):
        loadConfigFile('/Users/xiefangkui/WorkSpace/ustc2020/test/resource/config.json')

class SMSLogTest(unittest.TestCase):
    
    def test_send(self):
        doSMSLog(None, None)