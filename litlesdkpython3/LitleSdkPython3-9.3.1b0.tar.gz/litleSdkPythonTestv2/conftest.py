import pytest
from litleSdkPython.litleOnlineRequest import Configuration


@pytest.fixture(scope='session', autouse=True)
def config():
    config = Configuration()
    config.username = "jenkins"
    config.password = "PYTHON"
    config.merchantId = "101"
    config.reportGroup = 'DefaultReportGroup'
    config.url = 'Sandbox'
