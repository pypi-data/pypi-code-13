from sdk import *
import time

#TEST_DEBUG_URL_PREFIX = 'http://test_ckh_zyh.cloud.sensorsdata.cn:8006/sa?token=cfea25b78e758b3a' 
TEST_DEBUG_URL_PREFIX = 'http://test-ckh-zyh.cloud.sensorsdata.cn:8006/sa?token=de28ecf691865360'

consumer = DebugConsumer(TEST_DEBUG_URL_PREFIX, True)
sa = SensorsAnalytics(consumer, 'default', True)
sa.register_super_properties({'$app_version' : '1.0.1', 'hahah' : 123})

def inFunction():
    sa.track(1234, 'Test', {})

class XXX:

    def inClass(self):
        sa.track(1234, 'Test', {})

p = {'$time' : int(time.time() * 1000), 'aaa' : 123}
print(p)
sa.track(1234, 'Test', p)
print(p)
sa.track(1234, 'Test', p)
print(p)

inFunction()

XXX().inClass()
