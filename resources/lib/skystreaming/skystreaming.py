from http.client import Client
from parser.token_parser import TokenParser
from parser.error_parser import ErrorParser
from parser.playlist_parser import PlaylistParser
from exception.authentication_error import AuthenticationError
from exception.account_error import AccountError


class Skystreaming(object):
    def __init__(self):
        self._client = Client()
        self._token_parser = TokenParser()
        self._error_parser = ErrorParser()
        self._playlist_parser = PlaylistParser()

    def login(self, email, password):
        response = self._client.get('login')
        self._token_parser.feed(response.read())

        parameters = {
            '_token': self._token_parser.get_token(),
            'email': email,
            'password': password
        }

        response = self._client.post('signin', parameters)
        self._error_parser.feed(response.read())

        error_msg = self._error_parser.get_error()

        if error_msg != None:
            raise AuthenticationError('Authentication error', error_msg)

    def get_playlist(self):
        response = self._client.get('profilo')

        self._playlist_parser.feed(response.read())
        playlist_url = self._playlist_parser.get_playlist_url()

        if not playlist_url:
            raise AccountError('Premium account error')

        response = self._client.get_absolute(playlist_url)
        return response.read()
