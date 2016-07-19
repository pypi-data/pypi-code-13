from confmodel.fields import ConfigDict
from casepro.pods import Pod, PodConfig, PodPlugin


class DummyPodConfig(PodConfig):
    data = ConfigDict(
        "Data to show in the Pod's UI",
        required=True)


class DummyPod(Pod):
    def read_data(self, params):
        return self.config.data


class DummyPodPlugin(PodPlugin):
    label = 'dummy_pod'
    pod_class = DummyPod
    config_class = DummyPodConfig
    title = 'Dummy Pod'
