from setuptools import setup, find_packages
from os.path import join, dirname
import downloadMusicVK

setup(
    name='dwnlMusicVK',
    version=downloadMusicVK.__version__,
    packages=find_packages(),
    license='GNU',
    author='Akanoi',
    url=r'https://github.com/akanoi/DownloadMusicVK',
    description='Download all your music VK.',
    entry_points={
        'console_scripts':
            ['musicvk = downloadMusicVK.downloadMusic']
    }
)
