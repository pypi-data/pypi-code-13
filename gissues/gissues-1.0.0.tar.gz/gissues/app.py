from github3 import login, authorize
import os
import errno
from getpass import getpass

class App(object):

    PROGRAM_FOLDER = os.path.join(os.environ['HOME'], '.gissues')
    TOKEN_FILE = os.path.join(os.environ['HOME'], '.gissues', 'token.txt')

    def __init__(self):
        try:
            os.makedirs(App.PROGRAM_FOLDER)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise


        #If there isnt a token create one.
        if not os.path.exists(App.TOKEN_FILE):
            App.gissues_auth()

        token = App.read_token()


        #Login and init github3.py api with token
        self.gh = login(token=token)
        self.repo = None


    def gissues_auth():
        user = input("Type in your Github username: ")
        password = ''

        while not password:
            password = getpass("Password for {}: ".format(user))

        note = "GISSUES: View and manage Github issues."
        note_url = "https://github.com/DeveloperMal"
        scopes = ["user", "repo"]

        auth = authorize(user,
                         password,
                         scopes,
                         note,
                         note_url)

        with open(App.TOKEN_FILE, 'w') as tokenfile:
            tokenfile.write(auth.token + '\n')
            tokenfile.write(str(auth.id))

    def read_token():
        token = ''

        with open(App.TOKEN_FILE, 'r') as tokenfile:
            token = tokenfile.readline().strip()

        return token



#Global app object
app = App()
