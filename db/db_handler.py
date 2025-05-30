#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : db_handler.py
@Date    : 2025/5/29 10:40
@Author  : yaoxianda
@Version : 1.0
@Contact : 2386339350@qq.com
@License : (C) Copyright 2024-2024, yaoxianda.
@Desc    : What this script does.
数据处理层
"""

# 查询数据功能
import json
import os
from conf import setting


# 3.查看用户名是否存在
def select_data(username, data=True):  # 定义data=true时表示逻辑接口层需要返回数据
    # 1、接收逻辑接口层的username，并拼接用户名.json数据文件的路径
    user_path = os.path.join(
        setting.USER_DATA_DIR, f'{username}.json'
    )

    # 3.1判断用户名.json是否存在，如果存在，则提示用户重新输入
    if not os.path.exists(user_path):  # 用户不存在的情况，找不到用户json文件
        return
    if not data:  # 用户存在，且不需要用户数据时
        return True
    # 用户存在，且需要用户数据
    with open(user_path, mode='rt', encoding='utf-8') as f:
        user_data = json.load(f)
        return user_data

    # if os.path.exists(user_path) and not data:  # 逻辑接口层不需要返回数据时
    #     return True
    # elif os.path.exists(user_path) and data:
    #     with open(user_path, mode='rt', encoding='utf-8') as f:
    #         user_data = json.load(f)
    #         return user_data


# 保存用户数据
def save(user_data):
    # 1、接收user_data的username，并拼接用户名.json数据文件的路径
    username = user_data.get('username')
    user_path = os.path.join(
        setting.USER_DATA_DIR, f'{username}.json'
    )
    with open(user_path, mode='wt', encoding='utf-8') as f:
        json.dump(user_data, f, ensure_ascii=False)
