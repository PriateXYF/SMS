import zlib
import binascii
import struct
from module.api import Script
from typing import Annotated
class CheckImgSize(Script):
    """检测图片宽高是否正常，如不正常则计算正确的宽高"""

    def run(self, img: Annotated[str, "图片路径"]):
        image_data = open(img, 'rb')
        bin_data = image_data.read()
        crc32frombp = int(bin_data[29:33].hex(),16)
        # 使用函数计算
        crc32key = zlib.crc32(bin_data[12:29])
        # 对比算出的CRC和原本的CRC
        if crc32key == crc32frombp:
            return '宽高没有问题'
        else:
            # 宽度1-4000进行枚举
            for i in range(4000):
                # 高度1-4000进行枚举
                for j in range(4000):
                    data = bin_data[12:16] + \
                        struct.pack('>i', i) + struct.pack('>i', j) + bin_data[24:29]
                    crc32 = binascii.crc32(data) & 0xffffffff
                    # 计算当图片大小为i:j时的CRC校验值，与图片中的CRC比较，当相同，则图片大小已经确定
                    if(crc32 == crc32frombp):
                        print(i, j)
                        print('hex:', hex(i), hex(j))