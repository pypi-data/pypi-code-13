import requests


class Vibe(object):

    def __init__(self, key):
        """
        Initializing vibe api key
        PARAM
        -key : api key
        """
        if key:
            self.key = key
        else:
            print "Please Initialize with Key - You can do it by function change_key(key=<key>)"


    def change_key(self, key):
        """
        Function to change api key
        PARAM
        - key : api key
        """
        self.key = key


    def email(self, email, webhook_url=None):
        """
        Email lookup Function
        PARAM
        - email : lookup email
        - webhook_url : webhook url (Premium API users)
        """
        if webhook_url:
            info = requests.get("https://vibeapp.co/api/v1/profile_lookup/?key="+self.key+"&person_email="+email+"&webhook_url="+webhook_url)
        else:
            info = requests.get("https://vibeapp.co/api/v1/profile_lookup/?key="+self.key+"&person_email="+email)
        return info.json()


    def emailMD5(self, emailMD5):
        """
        EmailMD5 lookup Function
        PARAM
        - emailMD5 : lookup email hash
        """
        info = requests.get("https://vibeapp.co/api/v1/profile_lookup/?key="+self.key+"&email_md5="+emailMD5)
        return info.json()


    @property
    def get_stats(self):
        """
        Function to track your usage
        """
        stat = requests.get("https://vibeapp.co/api/v1/stats/?key="+self.key)
    	return stat.json()
