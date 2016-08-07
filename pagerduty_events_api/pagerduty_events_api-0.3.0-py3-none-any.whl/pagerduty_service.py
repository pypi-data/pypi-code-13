from pagerduty_events_api.pagerduty_incident import PagerdutyIncident


class PagerdutyService:
    def __init__(self, key):
        self.__service_key = key

    def get_service_key(self):
        return self.__service_key

    def trigger(self, description, additional_params={}):
        incident = PagerdutyIncident(self.__service_key)
        incident.trigger(description, additional_params)

        return incident
