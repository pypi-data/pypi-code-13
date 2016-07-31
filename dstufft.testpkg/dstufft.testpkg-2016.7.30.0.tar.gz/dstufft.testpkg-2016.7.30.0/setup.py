import setuptools

setuptools.setup(
    name="dstufft.testpkg",
    version="2016.07.30.0",
    packages=["dstufft_testpkg"],
    package_data={"dstufft_testpkg": ["data"]},
    # url="javascript:alert(0)",
    download_url="https://example.com/",
    contact="bah",
    contact_email="nope",
    fullname="thing",
    install_requires=[
        'GitPython>=1.0.1 # required for python 3 compat'],
)
