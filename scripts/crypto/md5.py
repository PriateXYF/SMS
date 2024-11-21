from module.api import Script
import hashlib
from typing import Annotated


class md5(Script):
    """对指定字符进行 MD5 加密"""

    def run(self, text: Annotated[str, "需要加密的文本"], encode: Annotated[str, "文本编码"] = "utf-8"):
        # 创建 MD5 哈希对象
        md5_obj = hashlib.md5()
        # 更新哈希对象（需要以字节形式传入）
        md5_obj.update(text.encode(encode))
        # 获取加密后的十六进制表示
        md5_hash = md5_obj.hexdigest()
        return md5_hash
