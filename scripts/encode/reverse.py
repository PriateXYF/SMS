from module.api import Script


class reverse(Script):
    """将给定字符串两个一组在前面添加 % 形成 URLEncode 格式字符串"""

    def run(self, text: str):
        return text[::-1]
