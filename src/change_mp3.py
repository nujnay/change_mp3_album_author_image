# -*- coding: utf8 -*-
import struct


def decode(x):  # 如果按照正常算法得到的synchsafe integer，解析成 真正的整数大小
    a = x & 0xff
    b = (x >> 8) & 0xff
    c = (x >> 16) & 0xff
    d = (x >> 24) & 0xff
    x_final = 0x0
    x_final = x_final | a
    x_final = x_final | (b << 7)
    x_final = x_final | (c << 14)
    x_final = x_final | (d << 21)
    return x_final


def encode(x):  # 和上边相反
    a = x & 0x7f
    b = (x >> 7) & 0x7f
    c = (x >> 14) & 0x7f
    d = (x >> 21) & 0x7f

    x_final = 0x0
    x_final = x_final | a
    x_final = x_final | (b << 8)
    x_final = x_final | (c << 16)
    x_final = x_final | (d << 24)
    return x_final


class MP3:
    def __init__(self, path):
        self.path = path
        pass

    def getInfo(self):
        fp = open(self.path, 'rb')
        head = fp.read(10)
        id3, ver, revision, flag, length = struct.unpack("!3sBBBI", head)
        length = decode(length)
        data = []
        while True:
            frame = fp.read(10)
            fid, size, flag, flag2 = struct.unpack("!4sI2B", frame)
            if size == 0:  # 有时候会留1024的白 不知道为啥
                break
            if ver == 4:  # 就是这一点 4和3的不同之处，4的这儿也采用synchsafe integer 了，注意啊
                size = decode(size)
            content = fp.read(size)
            data.append((fid, content))
            length -= (size + 10)
            print(length)

            if length <= 0:
                break
        fp.close()
        return data

    def buildItem(self, flag, content):
        content = content.decode('utf8').encode("utf16")
        content = struct.pack('!B', 1) + content
        length = len(content)
        head = struct.pack('!4sI2B', flag, length, 0, 0)
        return head + content

    def addImage(self, image, data):
        fp = open(self.path, 'rb')
        head = fp.read(10)
        try:
            id3, ver, revision, flag, length = struct.unpack("!3sBBBI", head)
        except:
            return False
        if id3 != 'ID3':
            return False
        # 新建立个文件
        fpNew = open(self.path + '.bak', "wb")
        fpImage = open(image, "rb")
        imageData = fpImage.read()  # 待用
        originLength = decode(length)  # 真实长度
        length = 0

        imageDataPre = struct.pack("!B10s2BB", 0, 'image/jpeg', 0, 0, 0)
        imageData = imageDataPre + imageData
        apicLen = len(imageData)  # 图片数据区域长度
        imageDataHead = struct.pack("!4sI2B", 'APIC', apicLen, 0, 0)
        imageData = imageDataHead + imageData

        TPE1 = self.buildItem('TPE1', data[u'Artist'].encode("utf8"))
        TIT2 = self.buildItem('TIT2', data[u'Title'].encode("utf8"))
        TALB = self.buildItem('TALB', data[u'Album'].encode("utf8"))

        # 新长度
        length += len(imageData)
        length += len(TPE1)
        length += len(TIT2)
        length += len(TALB)

        header = head[0:3]
        header += struct.pack('!B', 3)
        header += struct.pack('!H', 0)
        # 1字节留白
        header += struct.pack("!I", encode(length + 1))

        fpNew.write(header)
        fpNew.write(TPE1)
        fpNew.write(TIT2)
        fpNew.write(TALB)
        fpNew.write(imageData)
        fpNew.write(struct.pack('!B', 0))

        fp.seek(originLength, 1)  # 跳
        fpNew.write(fp.read())
        fpNew.close()
        fp.close()
        fpImage.close()

