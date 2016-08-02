from setuptools import setup


VERSION = "0.0.2"

setup(
    name='yandex-yaca-parser',
    description="Parse yandex yaca. See https://yandex.ru/yaca/?text=test",
    version=VERSION,
    url='https://github.com/KokocGroup/yandex-yaca-parser',
    download_url='https://github.com/KokocGroup/yandex-yaca-parser/tarball/v{0}'.format(VERSION),
    packages=['yandex_yaca_parser'],
)
