from time import sleep
from confmodel.fields import ConfigDict, ConfigBool
from casepro.pods import Pod, PodConfig, PodPlugin


class DummyPodConfig(PodConfig):
    data = ConfigDict(
        "Data to show in the Pod's UI",
        required=True)

    succeed = ConfigBool(
        "Whether or not the pod should load successfully (to demonstrate "
        "failure handling)",
        default=True)


class DummyPod(Pod):
    def read_data(self, params):
        if self.config.succeed:
            return self.config.data
        else:
            raise Exception('Dummy exception to demonstrate failure handling')

    def perform_action(self, type_, params):
        sleep(params.get('delay', 0))

        if params.get('succeed', True):
            return params['result']
        else:
            raise Exception('Dummy exception to demonstrate failure handling')


class DummyPodPlugin(PodPlugin):
    name = 'casepropods.dummy'
    label = 'dummy_pod'
    pod_class = DummyPod
    config_class = DummyPodConfig
    title = 'Dummy Pod'
