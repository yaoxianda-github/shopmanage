#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : setting.py
@Date    : 2025/5/28 10:38
@Author  : yaoxianda
@Version : 1.0
@Contact : 2386339350@qq.com
@License : (C) Copyright 2024-2024, yaoxianda.
@Desc    : What this script does.
配置信息
"""

# 获取项目根目录，为后续项目打包发布线上
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # 获取项目根目录
# print(BASE_DIR)
# USER_DATA_DIR = os.path.join(BASE_DIR, 'db', 'user_data')  # 获取默认user_data路径

CONFIG_PATH = os.path.join(BASE_DIR, 'setting.cfg')

import configparser

config = configparser.ConfigParser()
config.read(CONFIG_PATH, encoding='utf-8-sig')
USER_DATA_DIR = config.get('path', 'USER_DATA_DIR')  # 通过配置文件setting.cfg获取的路径
if not os.path.isdir(USER_DATA_DIR):  # 如果用户在setting.cfg中未配置路径，则用默认user_data路径
    USER_DATA_DIR = os.path.join(BASE_DIR, 'db', 'user_data')
print(USER_DATA_DIR)

# 获取goods_data路径
GOODS_DATA_DIR = os.path.join(BASE_DIR, 'db', 'goods_data')
# 获取提现手续费率
RATE = config.getfloat('bank', 'RATE')
