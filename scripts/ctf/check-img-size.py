import zlib
 
image_data=open('miku.png','rb')
bin_data=image_data.read()
crc32key = zlib.crc32(bin_data[12:29])                 #使用函数计算
if crc32key==int(bin_data[29:33].hex(), 16):#对比算出的CRC和原本的CRC
    print('宽高没有问题')
else:
    print('宽高被改了')