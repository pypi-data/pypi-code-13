

class FirebaseException(Exception):

    def __init__(self, error_code, error_message):
        super().__init__()
        self.code = error_code
        self.message = error_message
