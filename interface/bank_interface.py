#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : bank_interface.py
@Date    : 2025/5/28 10:35
@Author  : yaoxianda
@Version : 1.0
@Contact : 2386339350@qq.com
@License : (C) Copyright 2024-2024, yaoxianda.
@Desc    : What this script does.
银行相关接口

"""


# 充值接口
def recharge_interface(username, amount):
    # 获取用户数据
    from db import db_handler
    user_data = db_handler.select_data(username)
    # 给user_data里的balance充值操作
    user_data['balance'] += amount
    # 调用数据处理层，保存修改后的user_data数据
    db_handler.save(user_data)
    return True, f'用户{username}充值{amount}成功，' \
                 f'当前余额为：{user_data.get("balance")}'