#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A hodgepodge of utilities related to the app's settings and configuration.
"""
import os
from django.conf import settings
default_app_config = 'calaccess_raw.apps.CalAccessRawConfig'


def get_download_directory():
    """
    Returns download directory for data storage downloaded data.
    """
    if getattr(settings, 'CALACCESS_DOWNLOAD_DIR', None):
        return getattr(settings, 'CALACCESS_DOWNLOAD_DIR')
    elif getattr(settings, 'BASE_DIR', None):
        return os.path.join(getattr(settings, 'BASE_DIR'), 'data')
    raise ValueError("CAL-ACCESS download directory not configured. Set either \
CALACCESS_DOWNLOAD_DIR or BASE_DIR in settings.py")


def get_test_download_directory():
    """
    Returns download directory where we will store test data.
    """
    if getattr(settings, 'CALACCESS_TEST_DOWNLOAD_DIR', None):
        return getattr(settings, 'CALACCESS_TEST_DOWNLOAD_DIR')
    elif getattr(settings, 'BASE_DIR', None):
        return os.path.join(getattr(settings, 'BASE_DIR'), 'test-data')
    raise ValueError("CAL-ACCESS test download directory not configured. \
Set either CALACCESS_TEST_DOWNLOAD_DIR or BASE_DIR in settings.py")


def archive_directory_path(instance, filename):
    """
    Returns a path to an archived RawDataFile.

    (e.g., MEDIA_ROOT/YYYY-MM-DD_HH-MM-SS/filename.ext)
    """
    from calaccess_raw.models.tracking import RawDataVersion, RawDataFile

    if isinstance(instance, RawDataVersion):
        release_datetime = instance.release_datetime
    elif isinstance(instance, RawDataFile):
        release_datetime = instance.version.release_datetime
    else:
        raise TypeError("Must be called on RawDataVersion or RawDataFile instance.")
    template = '{dt.year}-{dt.month}-{dt.day}_{dt.hour}-{dt.minute}-{dt.second}/{f}'
    return template.format(dt=release_datetime, f=filename)


def get_model_list():
    """
    Returns a model list with all the data tables in this application.
    """
    from django.apps import apps
    model_list = apps.get_app_config("calaccess_raw").models.values()
    return [m for m in model_list if "CalAccessBaseModel" in str(m.__base__)]
