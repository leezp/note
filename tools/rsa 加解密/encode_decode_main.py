# -*- coding:utf-8 -*-
__author__ = 'leezp'
__date__ = 20210916
#  python3
# pip install rsa
# 资源包加密保护
# 输出 public.pem、private.pem、AES-KEY(RSA_Encrypted)、new_class.rules(AES_Encrypted file)
# eg: AES-KEY->  b'Nc0oko2eWm5/vRc+YzTHUuex0H7uRB/+d+KZRONcsf06WPLl08jDNeDjmiEFlbr2HNAngV7vUWQqTCUC14iocK+GOz6vsri+mvaajK0ar28esoZKYy2C1fGiRWAVnVQL1rHV3Q8AFP5fVnx6dr3DmAjpLJg54njdRbrSge/OL/g='
import re
import os


def merge():
    find_comment = re.compile(r'^#')
    for root, dirs, files in os.walk('./dir'):
        # 遍历文件
        for f in files:
            path = os.path.join(root, f)
            if '.rules' in path:
                f = open(path, "r", encoding='utf-8')
                for chunk in f.readlines():
                    if find_comment.search(chunk.strip()):
                        # print('发现注释 :' + chunk.strip())
                        continue
                    l = chunk.strip()
                    with open('new_class.txt', 'a', encoding='utf-8') as f:
                        f.write(l + '\n')


# 1. 合并未加密
# merge()
import rsa_decrypt


# 2. RSA 非对称加密
def RSA_encrypt():
    # 生成公私钥  等价于 http://web.chacuo.net/netrsakeypair
    def genRsaKey():
        import Crypto.PublicKey.RSA
        import Crypto.Random
        x = Crypto.PublicKey.RSA.generate(1024)
        a = x.publickey().exportKey()  # 生成公钥
        b = x.exportKey("PEM")  # 生成私钥
        with open("public.pem", "wb") as x:
            x.write(a)
        with open("private.pem", "wb") as x:
            x.write(b)

    genRsaKey()
    import random

    ## 加密的 plaintext 最大长度是 证书key位数/8 - 11, 例如1024 bit的证书，被加密的串最长 1024/8 - 11=117, 顺着这个思路google下，解决办法是 分块 加密，然后分块解密就行了，因为 证书key固定的情况下，加密出来的串长度是固定的

    # password = "1008612312345678"  # AES key 长度限制： 除了MODE_SIV模式key长度为：32, 48, or 64,其余key长度为16, 24 or 32
    password = "".join(random.choice("0123456789") for i in range(16))

    rsaUtil = rsa_decrypt.RsaUtil()
    encrypy_result = rsaUtil.encrypt_by_public_key(password)
    # print(encrypy_result)
    decrypt_result = rsaUtil.decrypt_by_private_key(encrypy_result)
    # print(decrypt_result)
    return encrypy_result, decrypt_result


RSA_encode_AES_key, AES_key = RSA_encrypt()
print("输出的en_AESkey为：")
print(RSA_encode_AES_key)

en_key_file = 'encode_AES.key'
with open(en_key_file, "wb") as x:
    x.write(RSA_encode_AES_key)

# 3. AES对称加密
"""
ECB没有偏移量
"""


def AES_encrypt_decrypt(AES_key, flag):
    from Crypto.Cipher import AES
    from binascii import b2a_hex, a2b_hex

    def add_to_16(text):
        if len(text.encode('utf-8')) % 16:
            add = 16 - (len(text.encode('utf-8')) % 16)
        else:
            add = 0
        text = text + ('\0' * add)
        return text.encode('utf-8')

    # 加密函数
    def encrypt(text):
        key = AES_key.encode('utf-8')
        # key = 'test_key'.encode('utf-8')
        mode = AES.MODE_ECB
        text = add_to_16(text)
        cryptos = AES.new(key, mode)

        cipher_text = cryptos.encrypt(text)
        return b2a_hex(cipher_text)

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(text):
        key = AES_key.encode('utf-8')
        # key = 'test_key'.encode('utf-8')
        mode = AES.MODE_ECB
        cryptor = AES.new(key, mode)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return bytes.decode(plain_text, encoding='utf-8', errors='ignore').rstrip('\0')

    # 加密，写文件
    if flag == 'enc':
        a = open('new_class.txt', encoding='utf-8').read()
        e = encrypt(a)

        with open('new_class.rules', 'w', encoding='utf-8') as f:
            f.write(e.decode('utf-8'))
    elif flag == 'dec':
        b = open('new_class.rules', encoding='utf-8').read()
        d = decrypt(b)  # 解密
        # print("解密:", d)
        # test new_class1.rules 与加密前的文件MD5一致
        with open('new_class1.rules', 'w', encoding='utf-8') as f:
            f.write(d)


AES_encrypt_decrypt(AES_key, 'enc')
# decrypt_result = rsa_decrypt.RsaUtil().decrypt_by_private_key(RSA_encode_AES_key)


decrypt_result2 = rsa_decrypt.RsaUtil().decrypt_by_private_key(open(en_key_file, encoding='utf-8').read())
print("解密后的AESkey为：")
print(decrypt_result2)
AES_encrypt_decrypt(decrypt_result2, 'dec')
