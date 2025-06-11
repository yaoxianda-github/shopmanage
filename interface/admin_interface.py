#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : admin_interface.py
@Date    : 2025/5/28 10:36
@Author  : yaoxianda
@Version : 1.0
@Contact : 2386339350@qq.com
@License : (C) Copyright 2024-2024, yaoxianda.
@Desc    : What this script does.

"""
from db import db_handler


# 冻结账户接口

def lock_user_interface(username):
    # 拿到用户数据
    user_data = db_handler.select_data(username)
    # 判断用户是否存在
    if not user_data:
        return False, f'\n用户{username}不存在！'
    if user_data.get('locked'):
        user_data['locked'] = False
        db_handler.save(user_data)
        return False, f'\n用户：{username}已解冻！'
    user_data['locked'] = True
    db_handler.save(user_data)
    return True, f'\n用户：{username}已冻结！'