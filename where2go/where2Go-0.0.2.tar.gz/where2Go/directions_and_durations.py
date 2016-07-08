import requests
import math
import json
from os.path import expanduser
from datetime import datetime
from bs4 import BeautifulSoup

GOOGLE_API_KEY = "AIzaSyC79GdoRDJXfeWDQnx5bBr14I3HJgEBIH0"


def get_current_coordinates():
    """
    Returns the current latitude and longitude
    defined by IP address
    """
    try:
        response = requests.get("http://ip-api.com/json")
        data = response.json()
        coordinates = (data['lat'], data['lon'])
    except requests.ConnectionError:
        print("Проблем с интернет връзката.")
        coordinates = (0, 0)
    return coordinates


def transform_html_directions(data):
    arr_instr = []
    # transform to text or put into json
    for leg in data['routes'][0]['legs']:
        for step in leg['steps']:
            arr_instr.append(step['html_instructions'])

    instructions = "\n".join(arr_instr)

    without_html = BeautifulSoup(instructions, 'html.parser')

    return without_html.get_text()


def get_duration(destination_lat, destination_lon):
    """
    Requires destination latitude and longitude
    Returns travel duration from the current position.
    If the status code of the response is not OK returns math.inf.
    """
    current_position = get_current_coordinates()

    url = ("https://maps.googleapis.com/maps/api/directions/"
           "json?origin={},{}&destination={},{}&key={}&"
           "language=bg&traffic_model").format(
        current_position[0], current_position[1],
        destination_lat, destination_lon, GOOGLE_API_KEY)

    try:
        response = requests.get(url)
        data = response.json()
    except requests.ConnectionError:
        print("Проблем с интернет връзката.")
        return math.inf

    if data['status'] == 'OK':
        return data['routes'][0]['legs'][0]['duration']['value']
    return math.inf


def get_duration_from_address(address, destination_lat, destination_lon):
    """
    Requires address (str) from which to calculate the travel duration and
    latitude and longitude of the destination
    """
    print(address)
    url = ("https://maps.googleapis.com/maps/api/directions/"
           "json?origin={}&destination={},{}&key={}&"
           "language=bg&traffic_model").format(
        address, destination_lat, destination_lon, GOOGLE_API_KEY)
    try:
        response = requests.get(url)
    except requests.ConnectionError:
        print("Проблем с интернет връзката.")
        return math.inf

    data = response.json()
    if data['status'] == 'OK':
        return data['routes'][0]['legs'][0]['duration']['value']
    return math.inf


def directions(destination_lat, destination_lon, address):
    if address is None:
        current_position = get_current_coordinates()
        url = ("https://maps.googleapis.com/maps/api/directions/"
               "json?origin={},{}&destination={},{}&key={}&"
               "language=bg".format(current_position[0],
                                    current_position[1], destination_lat,
                                    destination_lon, GOOGLE_API_KEY))
        try:
            response = requests.get(url)
        except requests.ConnectionError:
            print("Проблем с интернет връзката")
            return

    else:
        url = ("https://maps.googleapis.com/maps/api/directions/"
               "json?origin={}&destination={},{}&key={}&"
               "language=bg".format(address, destination_lat,
                                    destination_lon, GOOGLE_API_KEY))
        try:
            response = requests.get(url)
        except requests.ConnectionError:
            print("Проблем с интернет връзката.")
            return

    data = response.json()

    instructions = transform_html_directions(data)

    text_filename = "{}/{}_text.txt".format(
        expanduser("~"), str(datetime.now()).replace(":", "-"))

    with open(text_filename, 'w') as text_file:
        text_file.write(instructions)

    filename = "{}/{}.json".format(
        expanduser("~"), str(datetime.now()).replace(":", "-"))

    with open(filename, 'w') as json_file:
        json.dump(data, json_file)

    print(("В {} има записан json файл с инструкциите "
           "и текстов в {}").format(filename, text_filename))
