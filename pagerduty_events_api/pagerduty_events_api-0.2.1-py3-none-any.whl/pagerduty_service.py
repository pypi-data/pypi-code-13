from pagerduty_events_api.pagerduty_incident import PagerdutyIncident
from pagerduty_events_api.pagerduty_rest_client import PagerdutyRestClient


class PagerdutyService:
    def __init__(self, key):
        self.__service_key = key

    def get_service_key(self):
        return self.__service_key

    def trigger(self, description, additional_params={}):
        payload = {'service_key': self.__service_key,
                   'event_type': 'trigger',
                   'description': description}

        incident_data = PagerdutyRestClient().post(
            self.__append_additional_info_to_payload(payload, additional_params)
        )

        return PagerdutyIncident(self.__service_key, incident_data['incident_key'])

    @staticmethod
    def __append_additional_info_to_payload(mandatory_data, additional_data):
        return {**additional_data, **mandatory_data}
