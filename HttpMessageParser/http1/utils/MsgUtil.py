import json
from urllib.parse import unquote


class MsgUtil:

    @classmethod
    def parse_req_msg(cls, req_msg: str):
        line, header_str, body = cls.get_structure(req_msg)
        method, uri, _ = cls.parse_request_line(line)
        headers = cls.parse_header(header_str)

        params, parsed_body = None, None
        if method == "GET":
            params = cls.parse_get(uri)

        elif method == "POST":
            parsed_body = cls.parse_post(body, headers.get("Content-Type"))

        return method, uri, headers, params, parsed_body

    @classmethod
    def get_structure(cls, req_msg: str) -> tuple:
        line_end = req_msg.find("\n")
        header_end = req_msg.find("\n\n")
        line = req_msg[:line_end]
        header = req_msg[line_end + 1:header_end]
        body = "" if header_end == -1 else req_msg[header_end + 2:]
        return line, header, body

    @classmethod
    def parse_request_line(cls, line: str) -> list:
        return line.split(" ")

    @classmethod
    def parse_header(cls, header_str: str) -> dict:
        headers = {}
        kvs = header_str.split("\n")
        for kv in kvs:
            key, val = kv.split(": ", 1)
            headers[key] = val
        return headers

    @classmethod
    def parse_get(cls, uri: str):
        q_index = uri.find("?")
        if q_index == -1:
            return

        return cls.params_parse(uri[q_index + 1:])

    @classmethod
    def parse_post(cls, body: str, content_type: str):
        if not (content_type and body):
            return body

        semicolon = content_type.find(";")
        if semicolon != -1:  # exclude charset
            content_type = content_type[:semicolon]

        if content_type in ("text/xml", "application/xml"):
            return body

        if content_type == "application/json":
            return json.loads(body)

        if content_type in ("application/x-www-form-urlencoded", "multipart/form-data"):
            return cls.params_parse(body)

    @classmethod
    def params_parse(cls, params_string: str) -> dict:
        # for (url query params) and form parsing
        params = unquote(params_string).split("&")
        param_dict = {}
        for param in params:
            key, val = param.split("=")
            param_dict[key] = val
        return param_dict
