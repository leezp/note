# http://web.chacuo.net/netrsakeypair
# -*- coding: UTF-8 -*-
# ! /usr/bin/env python
import base64
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_v1_5_cipper
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA

import Crypto


# python3 不可加密过长的字符串，过长的需要分段加解密；


class RsaUtil(object):
    PUBLIC_KEY_PATH = 'public.pem'  # 公钥
    PRIVATE_KEY_PATH = 'private.pem'  # 私钥

    # 初始化key
    def __init__(self,
                 company_pub_file=PUBLIC_KEY_PATH,
                 company_pri_file=PRIVATE_KEY_PATH):

        if company_pub_file:
            self.company_public_key = RSA.importKey(open(company_pub_file).read())
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

    # 加密 支付方公钥
    def encrypt_by_public_key(self, encrypt_message):
        """使用公钥加密.
            :param encrypt_message: 需要加密的内容.
            加密之后需要对接过进行base64转码
        """
        encrypt_result = b''
        max_length = int(self.get_max_length(self.company_public_key))
        cipher = PKCS1_v1_5_cipper.new(self.company_public_key)
        while encrypt_message:
            input_data = encrypt_message[:max_length]
            encrypt_message = encrypt_message[max_length:]
            out_data = cipher.encrypt(input_data.encode(encoding='utf-8'))
            encrypt_result += out_data
        encrypt_result = base64.b64encode(encrypt_result)
        return encrypt_result

    # 加密 支付方私钥
    def encrypt_by_private_key(self, encrypt_message):
        """使用私钥加密.
            :param encrypt_message: 需要加密的内容.
            加密之后需要对接过进行base64转码
        """
        encrypt_result = b""
        max_length = int(self.get_max_length(self.company_private_key))
        cipher = PKCS1_v1_5_cipper.new(self.company_public_key)
        while encrypt_message:
            input_data = encrypt_message[:max_length]
            encrypt_message = encrypt_message[max_length:]
            out_data = cipher.encrypt(input_data.encode(encoding='utf-8').strip() + b"\n")
            encrypt_result += out_data
        encrypt_result = base64.b64encode(encrypt_result)
        return encrypt_result

    def decrypt_by_public_key(self, decrypt_message):
        """使用公钥解密.
            :param decrypt_message: 需要解密的内容.
            解密之后的内容直接是字符串，不需要在进行转义
        """
        decrypt_result = b""
        max_length = self.get_max_length(self.company_public_key, False)
        decrypt_message = base64.b64decode(decrypt_message)
        cipher = PKCS1_v1_5_cipper.new(self.company_public_key)
        while decrypt_message:
            input_data = decrypt_message[:max_length]
            decrypt_message = decrypt_message[max_length:]
            out_data = cipher.decrypt(input_data.encode(encoding='utf-8'), '')
            decrypt_result += out_data
        return decrypt_result

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
            #decrypt_result += str(out_data).strip()
			decrypt_result=out_data.decode()
            # decrypt_result += str(out_data).encode(encoding='utf-8').strip() + b"\n"
        return decrypt_result

    # 签名 商户私钥 base64转码
    def sign_by_private_key(self, message):
        """私钥签名.
            :param message: 需要签名的内容.
            签名之后，需要转义后输出
        """
        cipher = PKCS1_v1_5.new(self.company_private_key)  # 用公钥签名，会报错 raise TypeError("No private key") 如下
        # if not self.has_private():
        #   raise TypeError("No private key")
        hs = SHA.new(message)
        signature = cipher.sign(hs)
        return base64.b64encode(signature)

    def verify_by_public_key(self, message, signature):
        """公钥验签.
            :param message: 验签的内容.
            :param signature: 对验签内容签名的值（签名之后，会进行b64encode转码，所以验签前也需转码）.
        """
        signature = base64.b64decode(signature)
        cipher = PKCS1_v1_5.new(self.company_public_key)
        hs = SHA.new(message)

        # digest = hashlib.sha1(message).digest()  # 内容摘要的生成方法有很多种，只要签名和解签用的是一样的就可以

        return cipher.verify(hs, signature)


message = 'helloworld!'
print("明文内容：>>> ")
print(message)
rsaUtil = RsaUtil()
encrypy_result = rsaUtil.encrypt_by_public_key(message)
print("加密结果：>>> ")
print(encrypy_result)
decrypt_result = rsaUtil.decrypt_by_private_key(encrypy_result)
print("解密结果：>>> ")
print(decrypt_result)
sign = rsaUtil.sign_by_private_key(bytearray(message.encode(encoding='utf-8')))
print("签名结果：>>> ")
print(sign)
print("验签结果：>>> ")
print(rsaUtil.verify_by_public_key(bytearray(message.encode(encoding='utf-8')), sign))
