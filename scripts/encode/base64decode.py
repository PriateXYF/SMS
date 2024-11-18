import base64
from module.api import Script


class base64decode(Script):
    """对给定字符串进行 base64 解码"""

    def run(self, text: str, encode: str = "utf-8"):
        try:
            decoded_bytes = base64.b64decode(text.encode(encode))
            decoded_str = decoded_bytes.decode(encode)
        except Exception as e:
            return f"字符串不合法或编码不正确 : {e}"
        return decoded_str
