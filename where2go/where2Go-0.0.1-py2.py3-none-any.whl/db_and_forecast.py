from landmark import Landmark
from directions_and_durations import get_duration, get_duration_from_address
import sqlite3
import requests


WEATHER_API_ID = 'ad5d3d8d3760a601675b4a38170c6f6a'


def read_and_fill(category, address, days):
    """
    Reads the information about the landmarks from the chosen category.
    Returns a list of landmarks.
    """
    landmarks = []

    db_con = sqlite3.connect('where2Go/landmarks.db')
    db = db_con.cursor()

    for row in db.execute('SELECT * FROM {}'.format(category)):
        # row[1] and row[2] - coordinates of the landmark
        forecast_data = get_forecast_info(row[1], row[2], days)

        if forecast_data['list'][days - 1]['weather'][0]['main'] == 'Clear' or\
                forecast_data['list'][days - 1]['weather'][0]['main'] == \
                'Clouds':
            landmarks.append(Landmark(row[0], row[1], row[2]))

            # was forecast_data['list'][1]['clouds']['all'] before
            # forecast_data['list'][1]['temp']['day']['main']
            landmarks[-1].set_forecast_data(
                forecast_data['list'][days - 1]['clouds'],
                forecast_data['list'][days - 1]['temp']['day'])

            if address is None:
                duration = get_duration(row[1], row[2])
                landmarks[-1].set_travel_duration(duration)
            else:
                duration = get_duration_from_address(address, row[1], row[2])
                landmarks[-1].set_travel_duration(duration)

    return landmarks


def get_forecast_info(lat, lon, days):
    """
    Sends http requests to the weather api for the exact location
    and returns the response in json.
    """
    url = ("http://api.openweathermap.org/data/"
           "2.5/forecast/daily?lat={}&lon={}&cnt={}"
           "&units=metric&APPID={}").format(lat, lon, days, WEATHER_API_ID)
    print("Waiting for a response...")
    response = requests.get(url)

    forecast_data = response.json()
    return forecast_data


def sort_landmarks(landmarks):
    """
    First sorts the landmarks by the cloud percentage expectaion.
    After that sort them by temperature and after that by travel duration
    from the current position.
    Returns the sorted array of landmarks.
    """
    landmarks.sort(
        key=lambda landmark: landmark.get_cloud_percentage(), reverse=True)
    landmarks.sort(
        key=lambda landmark: landmark.get_average_temp(), reverse=True)
    landmarks.sort(
        key=lambda landmark: landmark.get_travel_duration())

    return landmarks
