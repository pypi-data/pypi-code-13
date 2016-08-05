import requests
import webbrowser


def make_request(endpoint, data):
    url = "https://api.foursquare.com/v2/venues/" + endpoint
    request = requests.get(url, params=data)
    display_results(request)

def display_results(request):
    user_input = raw_input("Do you want to see the results in the console or in the browser\n")
    while user_input != "console" and user_input != 'browser':
        print("This is a required field")
        user_input = input("Do you want to see the results in the console or in the browser\n")

    if user_input == 'console':
        print(request.json())
    else:
        webbrowser.open(request.url)
