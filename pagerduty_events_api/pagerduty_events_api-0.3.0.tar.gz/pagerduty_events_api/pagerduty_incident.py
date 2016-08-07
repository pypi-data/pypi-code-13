from pagerduty_events_api.pagerduty_rest_client import PagerdutyRestClient


class PagerdutyIncident:
    def __init__(self, service_key, incident_key=None):
        self.__service_key = service_key
        self.__incident_key = incident_key

    def get_service_key(self):
        return self.__service_key

    def get_incident_key(self):
        return self.__incident_key

    def acknowledge(self, additional_params={}):
        self.__modify_current_incident_with_event('acknowledge', additional_params)

    def resolve(self, additional_params={}):
        self.__modify_current_incident_with_event('resolve', additional_params)

    def trigger(self, description, additional_params={}):
        if self.__incident_key is None:
            self.__trigger_new_incident(description, additional_params)
        else:
            self.__trigger_existing_incident(description, additional_params)

    def __trigger_new_incident(self, description, additional_params={}):
        payload = {'service_key': self.__service_key,
                   'event_type': 'trigger',
                   'description': description}

        incident_data = PagerdutyRestClient().post(
            self.__append_additional_info_to_payload(payload, additional_params)
        )

        self.__incident_key = incident_data['incident_key']

    def __trigger_existing_incident(self, description, additional_params={}):
        additional_params['description'] = description
        self.__modify_current_incident_with_event('trigger', additional_params)

    def __modify_current_incident_with_event(self, event_type, additional_params={}):
        if self.__incident_key is None:
            raise AttributeError('No incident key was provided for {} action'.format(event_type))

        payload = {'service_key': self.__service_key,
                   'event_type': event_type,
                   'incident_key': self.__incident_key}

        PagerdutyRestClient().post(
            self.__append_additional_info_to_payload(payload, additional_params)
        )

    @staticmethod
    def __append_additional_info_to_payload(mandatory_data, additional_data):
        return {**additional_data, **mandatory_data}
