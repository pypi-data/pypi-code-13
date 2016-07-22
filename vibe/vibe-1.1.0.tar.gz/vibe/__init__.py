import requests


class Vibe(object):
    """docstring for Vibe"""

    def __init__(self, key=None):
        if key:
            self.key = key
        else:
            print "Please Initialize with Key - You can do it by function change_key(key=<key>)"


    def change_key(self, key):
        self.key = key


    def email(self, email):
        info = requests.get("https://vibeapp.co/api/v1/profile_lookup/?key="+self.key+"&person_email="+email)
        return info.json()


    def emailMD5(self, email):
        info = requests.get("https://vibeapp.co/api/v1/profile_lookup/?key="+self.key+"&email_md5="+email)
        return info.json()

    @property
    def get_stats(self):
        stat = requests.get("https://vibeapp.co/api/v1/stats/?key="+self.key)
    	return stat.json()
