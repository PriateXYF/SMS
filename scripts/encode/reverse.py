from module.api import Script
from typing import Annotated

class Reverse(Script):
    """将字符串倒序反转"""

    def run(self, text: Annotated[str, "需要处理的文本"]):
        return text[::-1]
