#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : user_interface.py
@Date    : 2025/5/28 10:34
@Author  : yaoxianda
@Version : 1.0
@Contact : 2386339350@qq.com
@License : (C) Copyright 2024-2024, yaoxianda.
@Desc    : What this script does.
用户相关接口
"""

from db import db_handler


# 用户注册接口

def register_interface(username, password, is_admin=False, balance=0):
    """
    注册接口，
    :param username:用户名 str
    :param password:密码 str
    :param balance:初始余额 int
    :param is_admin:是否是管理员，boolean
    :return:(boolean, str)
    """
    if db_handler.select_data(username, False):  # 调用数据处理层的查询用户功能，查询用户是否存在，且默认不需要返回用户数据
        return False, '\n用户名已存在！'  # 返回小元组
    # 组织用户数据字典
    user_data = {
        'username': username,
        'password': password,
        'balance': balance,
        'shopping_cart': {},
        'flow': [],
        'is_admin': is_admin,
        'locked': False,
    }
    # 调用数据处理层save方法，保存用户数据
    db_handler.save(user_data)
    return True, f'\n用户{username}注册成功！'


# 登录接口
def login_interface(username, password):
    user_data = db_handler.select_data(username)  # 查询用户是否存在
    # 用户不存在
    if not user_data:
        return False, f'\n用户: {username}不存在，请重新输入！', False
    # 校验用户密码
    if not password == user_data.get('password'):
        return False, f'\n用户名或者密码不正确，请重新输入！', False
    # 密码正确，校验用户是否为冻结状态
    if user_data.get('locked') is True:
        return False, f'\n用户: {username}已被冻结！', False
    return True, f'\n用户: {username}登录成功!', user_data.get('is_admin')
