class Landmark:
    """
    The class is a representation of a landmark.
    attributes:
        - __lat - latitude (coordinates), number
        - __lon - longitude (coordinates), number
        - __travel_duration - time needed to reach the place in seconds, number
        - __cloud_percentage - expected cloud perecentage in the place, number
        - __average_temp - expected average temperature in the place, number

    methods:
        - __init__(self, name, lat, lon) - initializer
            name - str, lat - number, lon - number
        - set_forecast_data(, cloud, average):
            cloud - number; cloud percentage
            average - number; average temperature
        - set_travel_duration(, duration):
            duration - time needed to reach the place, number
        - get_travel_duration():
            returns the time needed to reach the place in seconds
        - get_name():
            returns the name of the landmark - str
        - get_coordinates():
            returns a tuple of the latitude and longitute of the landmark
        - get_cloud_percentage():
            returns the expected cloud percentage - number
        - get_average_temp():
            returns the expected average temperature - number
    """
    __name = None
    __lat = 0
    __lon = 0
    __travel_duration = 0

    __cloud_percentage = 0
    __average_temp = 0

    def __init__(self, name, lat, lon):
        self.__name = name
        self.__lat = lat
        self.__lon = lon

    def set_forecast_data(self, cloud, average):
        self.__cloud_percentage = cloud
        self.__average_temp = average

    def set_travel_duration(self, duration):
        self.__travel_duration = duration

    def get_travel_duration(self):
        return self.__travel_duration

    def get_name(self):
        return self.__name

    def get_coordinates(self):
        """
        Returns a tuple of the latitude and longitute of the landmark
        """
        return (self.__lat, self.__lon)

    def get_cloud_percentage(self):
        return self.__cloud_percentage

    def get_average_temp(self):
        return self.__average_temp
