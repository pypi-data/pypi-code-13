import yaml


def serialize(requirements):
    f = open('./rqr.yaml', 'w')
    yaml.dump(requirements, f, default_flow_style=False)
    f.close()
