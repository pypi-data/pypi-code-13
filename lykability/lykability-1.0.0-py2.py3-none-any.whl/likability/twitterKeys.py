
class getKeys(object):

    def __init__(self):
        pass

    def keys():
        """Allows user to input tokens and keys to access Twitter API
	
        Returns:
            (token, tokenSecret, key, keysecret) (:obj: 'str'): Tuple containing API access credentials
            
            """
	
        token = input("Please enter access token: ")
        tokenSecret = input("Please enter access token secret: ")
        key = input("Please enter consumer key: ")
        keySecret = input("Please enter consumer key secret: ")

        return (token, tokenSecret, key, keySecret)
