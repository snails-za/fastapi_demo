import base64
import hashlib

from pypinyin import lazy_pinyin


class Base64Util:
    @staticmethod
    def encode(data: str) -> str:
        """对数据进行 Base64 编码"""
        byte_data = data.encode('utf-8')  # 将字符串转为字节
        encoded_data = base64.b64encode(byte_data)  # 编码
        return encoded_data.decode('utf-8')  # 返回字符串形式的 Base64 编码

    @staticmethod
    def decode(encoded_data: str) -> str:
        """对 Base64 编码的数据进行解码"""
        byte_data = encoded_data.encode('utf-8')  # 将字符串转为字节
        decoded_data = base64.b64decode(byte_data)  # 解码
        return decoded_data.decode('utf-8')  # 返回解码后的字符串


def get_hash(keyword: str) -> str:
    md5 = hashlib.md5()
    md5.update(keyword.encode('utf-8'))
    return md5.hexdigest()


def get_pinyin(name: str) -> str:
    py = lazy_pinyin(name)
    return py[0][0].lower() if py else '#'


# 使用示例
if __name__ == "__main__":
    text = "971011"

    # 编码
    encoded = Base64Util.encode(text)
    print(f"Encoded: {encoded}")

    # 解码
    decoded = Base64Util.decode(encoded)
    print(f"Decoded: {decoded}")

    print(get_hash("123456"))