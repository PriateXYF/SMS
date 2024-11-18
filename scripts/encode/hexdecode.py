from module.api import Script
import re


class hexdecode(Script):
    """将给定字符串两个一组在前面添加 % 形成 URLEncode 格式字符串"""

    def run(self, text: str, decode: str = "utf-8"):
        # 如果字符串包含百分号，先去掉百分号
        if "%" in text:
            text = re.sub(r"%([0-9A-Fa-f]{2})", lambda x: x.group(1), text)
        try:
            # 按16进制解码
            decoded_text = bytes.fromhex(text).decode(decode)
            return decoded_text
        except ValueError:
            return "字符串格式不正确，无法解码"
        except Exception as e:
            return e
