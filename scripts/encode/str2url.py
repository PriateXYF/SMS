from module.api import Script


class str2url(Script):
    """将给定字符串两个一组在前面添加 % 形成 URLEncode 格式字符串"""

    def run(self, str: str):
        ch_list = [f"%{str[i : i + 2]}" for i in range(0, len(str), 2)]
        return "".join(ch_list)
