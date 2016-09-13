class AuthenticationError(Exception):
    def __init__(self, message, http_message):
        self.message = message
        self.http_message = http_message

    def __str__(self):
        return self.message
