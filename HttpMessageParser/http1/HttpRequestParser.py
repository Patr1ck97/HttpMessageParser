import json
from typing import Any

import requests
from django.http.cookie import parse_cookie
from django.utils.datastructures import CaseInsensitiveMapping

template = """POST /dataFactory/index/ HTTP/1.1
Host: localhost:8000
User-Agent: python-requests/2.25.1
Accept-Encoding: gzip, deflate
Accept: */*
Content-Type: application/json
Cookie: csrftoken=7LN5cFEHCq3anK9rY34Qan32a1tzV4RxpCWrvmJOrIn0JpoSpAgZDYcqjsxvTLmz;
Content-Length: 15
Connection: keep-alive

{"test": "123"}"""


class HttpRequestParser:

    def __init__(self, req_msg: str):
        self._META = {"org_request_msg": req_msg}  # type: dict[str, Any]
        req_line, req_header, req_body = self.get_http_structure(req_msg)
        self.parse_request_line(req_line)
        self.parse_header(req_header)
        self.parse_body(req_body)
        pass

    @classmethod
    def get_http_structure(cls, req_msg):
        line_end = req_msg.find("\n")
        req_line = req_msg[:line_end]

        header_start = line_end + 1
        header_end = req_msg.find("\n\n")
        req_header = req_msg[header_start:header_end]

        body_start = header_end + 2
        req_body = req_msg[body_start:]

        return req_line, req_header, req_body

    def parse_request_line(self, line: str):
        method, uri, httpVersion = line.split(" ")
        self._META["method"] = method
        self._META["uri"] = uri
        self._META["http_version"] = httpVersion

    def parse_header(self, headers: str):
        header_map = {}
        kv_colons = headers.split("\n")
        for kv_colon in kv_colons:
            k, v = kv_colon.split(": ")
            header_map[k] = v
        self._META["headers"] = header_map
        self._META["url"] = header_map.get("Host") + self._META.get("uri")

    def parse_body(self, body):
        pass

    @property
    def META(self):
        return CaseInsensitiveMapping(self._META)

    @property
    def headers(self):
        return self._META.get("headers")

    @property
    def body(self):
        return

    @property
    def cookies(self):
        return parse_cookie(self.headers.get("Cookie"))


def main():
    req = HttpRequestParser(template)
    print(json.dumps(dict(req.META)))
    print(req.cookies)
    print(json.dumps(dict(req.headers)))


if __name__ == '__main__':
    main()
    # url = "http://127.0.0.1:8000/dataFactory/index/"
    # requests.post(url, headers={"Content-Type": "application/x-www-form-urlencoded"},
    #               data="name=test&age=23&realName=patrick")
