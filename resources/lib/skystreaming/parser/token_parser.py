from HTMLParser import HTMLParser


class TokenParser(HTMLParser, object):
    def __init__(self):
        super(TokenParser, self).__init__()
        self._token = None

    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            input_attrs = dict(attrs)
            if 'name' in input_attrs and input_attrs['name'] == '_token':
                self._token = input_attrs['value']

    def get_token(self):
        return self._token
