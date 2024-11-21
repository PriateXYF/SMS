import base64
from module.api import Script
from typing import Annotated

class Base64Decode(Script):
    """对给定字符串进行 base64 解码"""

    def run(self, text: Annotated[str, "需要解码的文本"], encode: Annotated[str, "文本编码"] = "utf-8"):
        try:
            decoded_bytes = base64.b64decode(text.encode(encode))
            decoded_str = decoded_bytes.decode(encode)
        except Exception as e:
            return f"字符串不合法或编码不正确 : {e}"
        return decoded_str
