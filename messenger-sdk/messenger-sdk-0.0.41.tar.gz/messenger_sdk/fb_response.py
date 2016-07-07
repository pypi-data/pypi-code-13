class FbResponse:
    def __init__(self, template=None):
        self._send = False
        self._templates = list()
        if template:
            self.add_template(template)

    def add_template(self, template):
        self._templates.append(template)

    @property
    def templates(self):
        return self._templates

    @property
    def send(self):
        return self._send

    @send.setter
    def send(self, condition: bool):
        self._send = condition
