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
from typing import Final
import zlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from .consts import TENANT_ID, Product


EMAIL_REGEX: Final = "^\\w+([-+.]\\w+)*@\\w+([-.]\\w+)*\\.\\w+([-.]\\w+)*$"


def get_random_string(length: int) -> str:
    letters = string.digits + string.ascii_lowercase + string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))


def get_random_device_id() -> str:
    return ''.join(random.choice('0123456789abcdef') for i in range(16))


def get_nonce() -> str:
    return get_random_string(32)


def get_timestamp() -> int:
    return int(time.time())


def get_timestamp_ms() -> int:
    return int(time.time() * 1000)


def get_enc_key() -> bytes:
    m = hashlib.md5()
    m.update(bytes(TENANT_ID, 'utf-8'))
    h = m.hexdigest()
    return bytes(h[8:24], 'utf-8')


def decrypt(data) -> str:
    cipher = Cipher(algorithms.AES128(get_enc_key()), modes.ECB())
    buf = cipher.decryptor().update(base64.b64decode(data))
    return str(buf[:-ord(buf[-1:])], 'utf-8')


def encrypt(data) -> str:
    cipher = Cipher(algorithms.AES128(get_enc_key()), modes.ECB())
    buf = bytes(data, 'utf-8')
    pad_len = 16 - (len(buf) % 16)
    buf = buf + bytes([pad_len]) * pad_len
    return base64.b64encode(cipher.encryptor().update(buf)).decode()


def get_map_enc_key(sn: str, mac: str, product_id: Product) -> bytes:
    sub_key = mac.replace(':', '').lower() + str(product_id.value)
    cipher = Cipher(algorithms.AES128(bytes(sub_key[0:16], 'utf-8')), modes.ECB())
    buf = bytes(sn + '+' + str(product_id.value) + '+' + sn, 'utf-8')
    pad_len = 16 - (len(buf) % 16)
    buf = buf + bytes([pad_len]) * pad_len

    key = base64.b64encode(cipher.encryptor().update(buf)).decode()

    m = hashlib.md5()
    m.update(bytes(key, 'utf-8'))
    h = m.hexdigest()
    return bytes(h[8:24], 'utf-8')


def decrypt_map(sn: str, mac: str, product_id: Product, data: bytes) -> bytes:
    key = get_map_enc_key(sn, mac, product_id)
    cipher = Cipher(algorithms.AES128(key), modes.ECB())
    buf = cipher.decryptor().update(base64.b64decode(data))
    try:
        return zlib.decompress(bytes.fromhex(str(buf[:-ord(buf[-1:])], 'utf-8')))
    except Exception:
        return bytes.fromhex(str(buf[:-ord(buf[-1:])], 'utf-8'))


def md5(data: str) -> str:
    m = hashlib.md5()
    m.update(bytes(data, 'utf-8'))
    return m.hexdigest()


def is_email(email: str) -> bool:
    return re.search(EMAIL_REGEX, email) is not None


def snake_case(value: str) -> str:
    first_underscore = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', first_underscore).lower()


def snake_case_fields(data: str) -> str:
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
