import base64
from module.api import Script
from typing import Annotated


def caesar_encrypt(text: str, offset: int):
    encrypted_string = ""
    for char in text:
        if char.isalpha():  # 检查是否为字母
            if char.islower():  # 小写字母
                encrypted_string += chr((ord(char) - ord("a") + offset) % 26 + ord("a"))
            elif char.isupper():  # 大写字母
                encrypted_string += chr((ord(char) - ord("A") + offset) % 26 + ord("A"))
        else:  # 非字母不处理
            encrypted_string += char
    return encrypted_string

class Caesar(Script):
    """对给定字符串进行凯撒加密"""
    def run(self,
            text: Annotated[str, "需要加密的文本"],
            offset: Annotated[int, "加密位移，如果为 0 则输出 1-25 的全部列表，默认为 0"] = 0
        ):
        if offset == 0:
            crypted_texts = [ caesar_encrypt(text, off) for off in range(1,26) ]
            return "\n".join(crypted_texts)
        return caesar_encrypt(text, offset)