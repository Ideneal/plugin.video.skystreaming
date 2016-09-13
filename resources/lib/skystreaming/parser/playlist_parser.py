from HTMLParser import HTMLParser


class PlaylistParser(HTMLParser, object):
    def __init__(self):
        super(PlaylistParser, self).__init__()
        self._is_playlist = False
        self._playlist_url = None

    def handle_starttag(self, tag, attrs):
        self._is_playlist = tag == 'textarea'

    def handle_data(self, data):
        if self._is_playlist:
            self._playlist_url = data
            self._is_playlist = False

    def get_playlist_url(self):
        return self._playlist_url
