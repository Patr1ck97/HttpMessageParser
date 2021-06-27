import json


class FileUtil:

    @classmethod
    def read_as_dict(cls, file) -> dict:
        string = cls.read_as_str(file)
        return json.loads(string)

    @classmethod
    def read_as_str(cls, file) -> str:
        with open(file, mode="r", encoding="utf-8") as f:
            return f.read()
