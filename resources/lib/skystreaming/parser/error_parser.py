from HTMLParser import HTMLParser


class ErrorParser(HTMLParser, object):
    def __init__(self):
        super(ErrorParser, self).__init__()
        self._error = None
        self._is_error = False

    def handle_starttag(self, tag, attrs):
        self._is_error = tag == 'h3'

    def handle_data(self, data):
        if self._is_error:
            self._error = data

    def get_error(self):
        return self._error
