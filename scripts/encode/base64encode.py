import base64
from module.api import Script


class base64encode(Script):
    """对给定字符串进行 base64 编码"""

    def run(self, str: str, encode: str = "utf-8"):
        encoded_bytes = base64.b64encode(str.encode(encode))
        encoded_str = encoded_bytes.decode(encode)
        return encoded_str
