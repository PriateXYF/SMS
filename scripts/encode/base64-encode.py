import base64
from module.api import Script
from typing import Annotated

class Base64Encode(Script):
    """对给定字符串进行 base64 编码"""

    def run(self, text: Annotated[str, "需要解码的文本"], encode: Annotated[str, "文本编码"] = "utf-8"):
        encoded_bytes = base64.b64encode(text.encode(encode))
        encoded_str = encoded_bytes.decode(encode)
        return encoded_str
