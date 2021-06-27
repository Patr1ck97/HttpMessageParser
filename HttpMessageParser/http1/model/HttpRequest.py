import json

from django.http import parse_cookie


class HttpRequest:

    def __init__(self, method, uri, headers, params, parsed_body, scheme="http"):
        self._method = method
        self._uri = uri
        self._scheme = scheme
        self._headers = headers
        self._params = params
        self._body = parsed_body

    @property
    def method(self):
        return self._method

    @property
    def url(self):
        return self._scheme + "://" + self._headers.get("Host") + self._uri

    @property
    def cookies(self):
        cookie = self._headers.get("Cookie")
        if not cookie:
            return {}
        return parse_cookie(cookie)

    @property
    def headers(self):
        return self._headers

    @property
    def params(self):
        return self._params

    @property
    def body(self):
        return self._body

    def __dict__(self):
        myDict = {}
        for attr in dir(self):
            if attr.startswith("__"):
                continue
            myDict[attr] = self.__getattribute__(attr)
        return myDict

    def __repr__(self):
        return json.dumps(self.__dict__(), ensure_ascii=False)


if __name__ == '__main__':
    httpRequest = HttpRequest(*('POST', '/', {'Host': '127.0.0.1:8080', 'User-Agent': 'python-requests/2.25.1',
                                              'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*',
                                              'Content-Type': 'application/json', 'hhh': '123', 'Content-Length': '41',
                                              'Connection': 'keep-alive'}, None,
                                {'test': '123', 'name': '[]*&*^%patrick'}))
    print(httpRequest)
