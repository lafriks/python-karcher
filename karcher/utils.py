# -----------------------------------------------------------
# Copyright (c) 2023 Lauris BH
# SPDX-License-Identifier: MIT
# -----------------------------------------------------------

import base64
import hashlib
import random
import re
import string
import time
import zlib
from Crypto.Cipher import AES

from .consts import TENANT_ID, Product


EMAIL_REGEX = "^\\w+([-+.]\\w+)*@\\w+([-.]\\w+)*\\.\\w+([-.]\\w+)*$"


def get_random_string(length):
    letters = string.digits + string.ascii_lowercase + string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))


def get_random_device_id():
    return ''.join(random.choice('0123456789abcdef') for i in range(16))


def get_nonce():
    return get_random_string(32)


def get_timestamp():
    return int(time.time())


def get_timestamp_ms():
    return int(time.time() * 1000)


def get_enc_key():
    m = hashlib.md5()
    m.update(bytes(TENANT_ID, 'utf-8'))
    h = m.hexdigest()
    return bytes(h[8:24], 'utf-8')


def decrypt(data):
    cipher = AES.new(get_enc_key(), AES.MODE_ECB)
    buf = cipher.decrypt(base64.b64decode(data))
    return str(buf[:-ord(buf[-1:])], 'utf-8')


def encrypt(data):
    cipher = AES.new(get_enc_key(), AES.MODE_ECB)
    buf = bytes(data, 'utf-8')
    pad_len = cipher.block_size - (len(buf) % cipher.block_size)
    buf = buf + bytes([pad_len]) * pad_len
    return base64.b64encode(cipher.encrypt(buf)).decode()


def get_map_enc_key(sn: str, mac: str, product_id: Product):
    sub_key = mac.replace(':', '').lower() + str(product_id.value)
    cipher = AES.new(bytes(sub_key[0:16], 'utf-8'), AES.MODE_ECB)
    buf = bytes(sn + '+' + str(product_id.value) + '+' + sn, 'utf-8')
    pad_len = cipher.block_size - (len(buf) % cipher.block_size)
    buf = buf + bytes([pad_len]) * pad_len

    key = base64.b64encode(cipher.encrypt(buf)).decode()

    m = hashlib.md5()
    m.update(bytes(key, 'utf-8'))
    h = m.hexdigest()
    return bytes(h[8:24], 'utf-8')


def decrypt_map(sn: str, mac: str, product_id: Product, data: bytes):
    cipher = AES.new(get_map_enc_key(sn, mac, product_id), AES.MODE_ECB)
    buf = cipher.decrypt(base64.b64decode(data))
    try:
        return zlib.decompress(bytes.fromhex(str(buf[:-ord(buf[-1:])], 'utf-8')))
    except Exception:
        return bytes.fromhex(str(buf[:-ord(buf[-1:])], 'utf-8'))


def md5(data):
    m = hashlib.md5()
    m.update(bytes(data, 'utf-8'))
    return m.hexdigest()


def is_email(email):
    return re.search(EMAIL_REGEX, email) is not None


def snake_case(value):
    first_underscore = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', first_underscore).lower()


def snake_case_fields(data):
    if type(data) is dict:
        n = {}
        for k, v in data.items():
            n[snake_case(k)] = snake_case_fields(v)
        return n
    elif type(data) is list:
        n = []
        for v in data:
            n.append(snake_case_fields(v))
        return n
    else:
        return data
