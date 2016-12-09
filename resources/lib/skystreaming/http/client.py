import urllib
import urllib2
import cookielib


class Client(object):
    BASE_URL = 'https://skystreaming.cc/'

    DEFAULT_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}

    def __init__(self):
        self.cookies = cookielib.LWPCookieJar()
        self.handlers = (urllib2.HTTPHandler(), urllib2.HTTPSHandler(), urllib2.HTTPCookieProcessor(self.cookies))
        self.opener = urllib2.build_opener(*self.handlers)

    def get(self, path):
        request = urllib2.Request(self.BASE_URL + path, headers=self.DEFAULT_HEADERS)
        return self.opener.open(request)

    def post(self, path, params):
        data = urllib.urlencode(params)
        request = urllib2.Request(self.BASE_URL + path, data=data, headers=self.DEFAULT_HEADERS)
        return self.opener.open(request)

    def get_absolute(self, url):
        request = urllib2.Request(url, headers=self.DEFAULT_HEADERS)
        return self.opener.open(request)

    def post_absolute(self, url, params):
        data = urllib.urlencode(params)
        request = urllib2.Request(url, data=data, headers=self.DEFAULT_HEADERS)
        return self.opener.open(request)
