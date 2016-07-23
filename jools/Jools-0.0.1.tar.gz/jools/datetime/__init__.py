#!/usr/bin/python3
# -*- coding: utf-8 -*-

import calendar
from datetime import timedelta, datetime


def add_seconds(source_datetime: datetime, seconds: int) -> datetime:
    """
    :type source_datetime: datetime object
    :param seconds: the amount of seconds the source_datetime should be increased or decreased by
                     Quantity can be a positive and a negative number
    :return: datetime object increased with a number of seconds
    """
    return source_datetime + timedelta(seconds=seconds)


def add_minutes(source_datetime: datetime, minutes: int) -> datetime:
    """
    :type source_datetime: datetime object
    :param minutes: the amount of minutes the source_datetime should be increased or decreased by
                     Quantity can be a positive and a negative number
    :return: datetime object increased with a number of minutes
    """
    return source_datetime + timedelta(minutes=minutes)


def add_hours(source_datetime: datetime, hours: int) -> datetime:
    """
    :type source_datetime: datetime object
    :param hours: the amount of hours the source_datetime should be increased or decreased by
                     Quantity can be a positive and a negative number
    :return: datetime object increased with a number of hours
    """
    return source_datetime + timedelta(hours=hours)


def add_days(source_datetime: datetime, days: int) -> datetime:
    """
    :type source_datetime: datetime object
    :param days: the amount of days the source_datetime should be increased or decreased by
                     Quantity can be a positive and a negative number
    :return: datetime object increased with a number of days
    """
    return source_datetime + timedelta(days=days)


def add_weeks(source_datetime: datetime, weeks: int) -> datetime:
    """
    :type source_datetime: datetime object
    :param weeks: the amount of weeks the source_datetime should be increased or decreased by
                     Quantity can be a positive and a negative number
    :return: datetime object increased with a number of weeks
    """
    return source_datetime + timedelta(weeks=weeks)


def add_months(source_datetime: datetime, months: int) -> datetime:
    """
    :type source_datetime: datetime object
    :param months: the amount of months the source_datetime should be increased or decreased by
                     Quantity can be a positive and a negative number
    :return: datetime object increased with a number of months
    """
    month = source_datetime.month - 1 + months
    year = int(source_datetime.year + month / 12)
    month = month % 12 + 1
    day = min(source_datetime.day, calendar.monthrange(year, month)[1])
    return datetime(year, month=month, day=day, hour=source_datetime.hour,
                    minute=source_datetime.minute, second=source_datetime.second)


def add_years(source_datetime: datetime, years: int) -> datetime:
    """
    :type source_datetime: datetime object
    :param years: the amount of years the source_datetime should be increased or decreased by
                     Quantity can be a positive and a negative number
    :return: datetime object increased with a number of years
    """
    return add_months(source_datetime, months=years*12)
