import anvil.server

def get_user_email():
    return anvil.server.call("anvil.private.google.auth.get_user_email")
