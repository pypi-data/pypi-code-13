import os
import json


class Settings(dict):

    def __init__(self, app, rules):
        for key, rule in rules.items():
            raw, default = os.environ.get("FLASK_{0}".format(key)), None
            if isinstance(rule, tuple):
                rule, default = rule
            if raw is None:
                if default is None:
                    raise ValueError("{0}: not defined".format(key))
                else:
                    value = default
            else:
                if rule != str:
                    value = json.loads(raw)
                    if not isinstance(value, rule):
                        raise ValueError("Invalid '{0}' type: '{1}".format(
                            key, type(value)
                        ))
                else:
                    value = raw
            self[key] = value
        app.config.update(self)
