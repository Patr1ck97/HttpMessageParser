from unittest import TestCase

from HttpMessageParser.http1.model.HttpRequest import HttpRequest
from HttpMessageParser.http1.utils.FileUtil import FileUtil
from HttpMessageParser.http1.utils.MsgUtil import MsgUtil


class TestMsgUtil(TestCase):

    def setUp(self) -> None:
        self.req_msg = FileUtil.read_as_str(r"../templates/request.txt")
        self.json_msg = FileUtil.read_as_str(r"../templates/meta.json")
        print("===begin===")

    def test_parse_req_msg(self):
        res = MsgUtil.parse_req_msg(self.req_msg)
        httpRequest = HttpRequest(*res)
        print(res)
        print(httpRequest)

    def tearDown(self) -> None:
        print("===end===")
