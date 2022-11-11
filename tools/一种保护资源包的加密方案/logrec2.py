# cython: language_level=3
# -*- coding:utf-8 -*-
__author__ = 'leezp'
__date__ = 20220711
import base64
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_v1_5_cipper
from Crypto.PublicKey import RSA
import Crypto
import os
import hashlib

PRIVATE_KEY_PATH = '/***/private.pem'
en_key_file = '/***/encode_AES.key'


def GetFileMd5(filename):
    if os.path.isfile(filename):
        fp = open(filename, 'rb')
        contents = fp.read()
        fp.close()
        md5 = hashlib.md5(contents).hexdigest()
    else:
        print('file not exists')
    return md5


def judgefile(filepath):
    if os.path.isfile(filepath):
        a = GetFileMd5(filepath)
        if a == "0713ae0a726ad7bcb2f20e7ff524c523":
            pass
        else:
            exit(1)
    else:
        exit(1)


judgefile("./***.py") # 调用时注意绝对路径与相对路径，尽量使用绝对路径


class log(object):

    # 初始化key
    def __init__(self,
                 company_pri_file=PRIVATE_KEY_PATH):
        if company_pri_file:
            self.company_private_key = RSA.importKey(open(company_pri_file).read())

    def get_max_length(self, rsa_key, encrypt=True):
        """加密内容过长时 需要分段加密 换算每一段的长度.
            :param rsa_key: 钥匙.
            :param encrypt: 是否是加密.
        """
        blocksize = Crypto.Util.number.size(rsa_key.n) / 8
        reserve_size = 11  # 预留位为11
        if not encrypt:  # 解密时不需要考虑预留位
            reserve_size = 0
        maxlength = blocksize - reserve_size
        return maxlength

    def decrypt_by_private_key(self, decrypt_message):
        """使用私钥解密.
            :param decrypt_message: 需要解密的内容.
            解密之后的内容直接是字符串，不需要在进行转义
        """
        # decrypt_result = b""
        decrypt_result = ""
        max_length = int(self.get_max_length(self.company_private_key, False))
        decrypt_message = base64.b64decode(decrypt_message)
        cipher = PKCS1_v1_5_cipper.new(self.company_private_key)
        while decrypt_message:
            input_data = decrypt_message[:max_length]
            decrypt_message = decrypt_message[max_length:]
            out_data = cipher.decrypt(input_data, '')
            # decrypt_result += str(out_data).encode(encoding='utf-8').strip()
            # decrypt_result += str(out_data).strip()
            decrypt_result = out_data.decode()
            # decrypt_result += str(out_data).encode(encoding='utf-8').strip() + b"\n"
        return decrypt_result

    def AES_encrypt_decrypt(self, AES_key, flag):
        from Crypto.Cipher import AES
        from binascii import a2b_hex
        # 解密后，去掉补足的空格用strip() 去掉
        def decrypt(text):
            key = AES_key.encode('utf-8')
            mode = AES.MODE_ECB
            cryptor = AES.new(key, mode)
            plain_text = cryptor.decrypt(a2b_hex(text))
            return bytes.decode(plain_text, encoding='utf-8', errors='ignore').rstrip('\0')

        if flag == 'dec':
            b = open('/***.rules', encoding='utf-8').read()
            d = decrypt(b)  # 解密
            return d

    def getcontent(self):
        decrypt_result2 = self.decrypt_by_private_key(open(en_key_file, encoding='utf-8').read())
        plain_text = self.AES_encrypt_decrypt(decrypt_result2, 'dec')
        return plain_text
