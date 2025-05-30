#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : common.py
@Date    : 2025/5/28 10:37
@Author  : yaoxianda
@Version : 1.0
@Contact : 2386339350@qq.com
@License : (C) Copyright 2024-2024, yaoxianda.
@Desc    : What this script does.
公共方法
"""


# 登录认证装饰器

def login_auth(func):
    def wrapper(*args, **kwargs):
        from core import src
        if src.logged_user:
            res = func(*args, **kwargs)
            return res
        else:
            print('\n请先登录吧！')
            src.login()

    return wrapper


# 密码加密
import hashlib


def pwd_to_sha256(password):
    # 创建一个SHA-256对象
    sha256_hash = hashlib.sha256()
    # 将密码字符串编码为字节流后传入SHA-256对象
    sha256_hash.update(password.encode('utf-8'))
    sha256_hash.update('两只老虎跑得快'.encode('gbk'))  # 加点盐，提高密码安全性
    # 获取加密后的十六进制表示形式
    hashed_password = sha256_hash.hexdigest()
    return hashed_password
