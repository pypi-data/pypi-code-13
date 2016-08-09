"""
________________________________________________________________________________

flask.

 /$$      /$$  /$$$$$$   /$$$$$$  /$$$$$$  /$$$$$$
| $$$    /$$$ /$$__  $$ /$$__  $$|_  $$_/ /$$__  $$
| $$$$  /$$$$| $$  \ $$| $$  \__/  | $$  | $$  \__/
| $$ $$/$$ $$| $$$$$$$$| $$ /$$$$  | $$  | $$
| $$  $$$| $$| $$__  $$| $$|_  $$  | $$  | $$
| $$\  $ | $$| $$  | $$| $$  \ $$  | $$  | $$    $$
| $$ \/  | $$| $$  | $$|  $$$$$$/ /$$$$$$|  $$$$$$/
|__/     |__/|__/  |__/ \______/ |______/ \______/

https://github.com/mardix/flask-magic

________________________________________________________________________________
"""



from flask_magic import MagicWand, get_env, get_env_app, import_module

# import the application's views.py dynamically from the app environment
# The app environment is set as: app=$app_name:$environment
# ie: app=www:production

app_name = get_env_app() or "{project_name}"

app_view = "application.%s" % app_name

import_module(app_view)

# 'app' variable name is required if you intend to use 'Magic' the cli tool
app = MagicWand(__name__, project=app_name)

