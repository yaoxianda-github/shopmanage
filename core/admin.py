#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : admin.py
@Date    : 2025/6/10 15:11
@Author  : yaoxianda
@Version : 1.0
@Contact : 2386339350@qq.com
@License : (C) Copyright 2024-2024, yaoxianda.
@Desc    : What this script does.

管理员视图层主程序

"""

from core import src
from interface import admin_interface


# 添加账户
def add_user():
    print('\n添加账户')
    is_admin = input('\n是否添加管理员(y or n):').strip().lower()
    if is_admin == 'y':
        src.register(True)
    else:
        src.register()


# 冻结账户
def lock_user():
    print('\n冻结账户')
    while True:
        # 接收管理员输入的用户名
        lock_username = input('\n请输入需要冻结的账户名：').strip()
        is_locked = input('\n按任意键确认/n退出：').strip().lower()
        if lock_username == src.logged_user:
            print('\n管理员不可以冻结自己！')
            continue
        if is_locked == 'n':
            break
        # 调用冻结账户接口进行冻结账户操作
        flag, msg = admin_interface.lock_user_interface(lock_username)
        print(msg)
        if flag:
            break


# 给用户充值
def recharge_to_user():
    username = input('\n请输入需要充值的用户名：').strip()
    src.recharge(username)


func_dict = {
    '0': ('返回首页',),
    '1': ('添加账户', add_user),
    '2': ('冻结账户', lock_user),
    '3': ('给用户充值', recharge_to_user)

}


def main():
    while True:
        print('管理员功能'.center(20, '='))
        for num in func_dict:
            print(f'{num} {func_dict.get(num)[0]}'.center(20, ' '))
        print('我也是有底线的'.center(20, '='))
        opt = input('请输入功能编号：').strip()
        if opt not in func_dict:
            print('此功能不存在')
            continue
        if opt == '0':
            break
        func_dict.get(opt)[1]()  # 拿到函数名加括号，执行对应功能函数
