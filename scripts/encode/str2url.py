from module.api import Script
from typing import Annotated

class str2url(Script):
    """将给定字符串两个一组在前面添加 % 形成 URLEncode 格式字符串"""

    def run(self, text: Annotated[str, "需要处理的文本"]):
        ch_list = [f"%{text[i : i + 2]}" for i in range(0, len(text), 2)]
        return "".join(ch_list)
