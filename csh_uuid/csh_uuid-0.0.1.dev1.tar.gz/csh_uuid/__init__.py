import requests

base_url = "https://uid.csh.rit.edu"


def get_uuid_from_uid(uid):
    r = requests.get(base_url + "/uuid/" + uid)
    if r.status_code == 200:
        return r.content.decode('utf-8')
    else:
        return False


def get_uid_from_uuid(uuid):
    r = requests.get(base_url + "/uid/" + uuid)
    if r.status_code == 200:
        return r.content.decode('utf-8')
    else:
        return False
