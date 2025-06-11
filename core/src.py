#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : src.py
@Date    : 2025/5/28 10:32
@Author  : yaoxianda
@Version : 1.0
@Contact : 2386339350@qq.com
@License : (C) Copyright 2024-2024, yaoxianda.
@Desc    : What this script does.
        用户视图层

"""

from interface import user_interface, bank_interface
from lib import common

logged_user = None  # 记录用户登录状态
logged_admin = False  # 是否管理员


# 0、用户退出
def sign_out():
    print('\n感谢使用，欢迎下次光临')
    exit()


# 1、注册功能
def register(is_admin=False):
    while True:
        print('\n注册')
        username = input('请输入用户名：').strip()
        password = input('请输入密码：').strip()
        re_password = input('请确认密码：').strip()
        is_register = input('按任意键确认/按键盘上的字母n退出：').strip().lower()

        # 1、判断用户是否想退出
        if is_register == 'n':
            break
        # 2、判断两次输入的密码是否一致
        if password != re_password:
            print('\n 两次输入密码不一致！')
            continue
        # 2.1判断用户名是否合法
        import re
        if not re.findall('[a-zA-Z]\w{2,9}$', username):
            print('\n用户名长度必须为3-10个字符！\n只能由字母，数字，下划线组成，并只能以字母开头')
            continue
        # 2.2校验密码强度
        # if not re.findall('^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,16}$', password):
        #     print('\n密码太弱了，必须包含大写字母，小写字母和数字，且长度必须为8到16位')
        #     continue

        # 3、密码加密
        password = common.pwd_to_sha256(password)

        # 4、调用注册接口进行注册
        flag, msg = user_interface.register_interface(username, password, is_admin)  # 接收小元组，进行解压赋值
        print(msg)
        if flag:  # 注册成功，终止循环
            break

        # # 3.查看用户名是否存在-----数据处理层
        # import json
        # import os
        # from conf import setting
        # user_path = os.path.join(
        #     setting.USER_DATA_DIR, f'{username}.json'
        # )
        # # 3.1如果存在，则提示用户重新输入
        # if os.path.exists(user_path):
        #     print('\n用户名已存在！')
        #     continue
        # # 3.2如果不存在，则保存用户数据,以json文件形式存用户数据-----新增逻辑处理接口--注册接口
        # user_data = {
        #     'username': username,
        #     'password': password,
        #     'balance': 0,
        #     'shopping_cart': [],
        #     'flow': [],
        #     'is_admin': False,
        #     'locked': False,
        # }
        #
        # # 将用户数据保存成文件----数据处理层
        # with open(user_path, mode='wt', encoding='utf-8') as f:
        #     json.dump(user_data, f, ensure_ascii=False)
        # break


# 2、登录功能
def login():
    while True:
        # 1、让用户输入用户名和密码
        username = input('\n请输入用户名：').strip()
        password = input('\n请输入密码：').strip()
        is_login = input('\n按任意键确定或者按/n退出').strip().lower()
        if is_login == 'n':  # 判断用户是否想退出登录功能
            break
        # 2、密码加密
        password = common.pwd_to_sha256(password)

        # 3、调用逻辑接口层，把数据传给登录接口，接口再调用数据处理层的方法校验用户是否存在
        flag, msg, is_admin = user_interface.login_interface(username, password)
        print(msg)
        if flag:
            global logged_user, logged_admin
            logged_user = username
            logged_admin = is_admin
            break


# 3、充值功能
@common.login_auth
def recharge(username=False):
    print('充值功能')
    while True:
        amount = input('请输入充值金额：').strip()
        is_recharge = input('按任意键确认/n退出').strip().lower()
        # 允许用户退出充值功能
        if is_recharge == 'n':
            break
        # 判断用户输入的金额是否是数字
        if not amount.isdigit():
            print('\n请输入正确的金额！')
            continue
        # 把amount转为int类型
        amount = int(amount)
        # 判断用户输入金额是否为0
        if amount == 0:
            print('\n充值的金额不能为0！')
            continue
        # 调用充值接口进行充值
        if not username:
            username=logged_user
        flag, msg = bank_interface.recharge_interface(username, amount)
        print(msg)
        if flag:
            break


# 4、转账功能
@common.login_auth
def transfer():
    print('转账功能')
    while True:
        # 接收用户输入的用户名和转账金额
        to_username = input('\n请输入转账目标用户的用户名：').strip()
        amount = input('\n请输入转账金额：').strip()
        is_transfer = input('\n按任意键确认/n退出').strip().lower()
        # 允许用户退出转账功能
        if is_transfer == 'n':
            break
        # 判断用户输入的金额是否是数字
        if not amount.isdigit():
            print('\n请输入正确的金额！')
            continue
        # 把amount转为int类型
        amount = int(amount)
        # 判断用户输入金额是否为0
        if amount == 0:
            print('\n转账的金额不能为0！')
            continue
        # 判断用户是否给自己转账
        if logged_user == to_username:
            print('\n不能给自己转账！')
            continue

        # 调用转账接口进行转账
        flag, msg = bank_interface.transfer_interface(logged_user, to_username, amount)
        print(msg)
        if flag:
            break


# 5、提现功能
@common.login_auth
def withdraw():
    print('提现功能')
    while True:
        amount = input('请输入提现金额：').strip()
        is_withdraw = input('按任意键确认/n退出').strip().lower()
        # 允许用户退出提现功能
        if is_withdraw == 'n':
            break
        # 判断用户输入的金额是否是数字
        if not amount.isdigit():
            print('\n请输入正确的金额！')
            continue
        # 把amount转为int类型
        amount = int(amount)
        # 判断用户输入金额是否小于500
        if amount < 500:
            print('\n提现的金额不能小于500！')
            continue
        # 调用提现接口进行提现

        flag, msg = bank_interface.withdraw_interface(logged_user, amount)
        print(msg)
        if flag:
            break


# 6、查看余额
@common.login_auth
def check_balance():
    print('查看余额')
    flag, msg = bank_interface.check_balance_interface(logged_user)
    print(msg)


# 7、查看流水
@common.login_auth
def check_flow():
    print('查看流水')
    flag, flow_list = bank_interface.check_flow_interface(logged_user)
    if not flow_list:
        print('\n该用户没有流水！')
    for flow in flow_list:
        print(flow)


# 8、购物功能
@common.login_auth
def shopping():
    print('购物功能')


# 9、查看购物车功能
@common.login_auth
def check_shopping_cart():
    print('查看购物车')


# 10、退出账号
@common.login_auth
def login_out():
    print('退出账号')
    global logged_user, logged_admin
    print(f'用户: {logged_user}已退出')
    logged_user = None
    logged_admin = False


# 11、管理员功能
@common.login_auth
def admin():
    print('管理员功能')
    from core import admin
    admin.main()


# 函数字典
func_dict = {
    '0': ('退出功能', sign_out),
    '1': ('注册功能', register),
    '2': ('登录功能', login),
    '3': ('充值功能', recharge),
    '4': ('转账功能', transfer),
    '5': ('提现功能', withdraw),
    '6': ('查看余额', check_balance),
    '7': ('查看流水', check_flow),
    '8': ('购物功能', shopping),
    '9': ('查看购物车', check_shopping_cart),
    '10': ('退出账号', login_out),
    '11': ('管理员功能', admin)

}


# 主程序
def main():
    while True:
        print('购物管理系统'.center(20, '='))
        for num in func_dict:
            if logged_admin:
                print(f'{num} {func_dict.get(num)[0]}'.center(20, ' '))
            else:
                if num != '11':
                    print(f'{num} {func_dict.get(num)[0]}'.center(20, ' '))
        print('我也是有底线的'.center(20, '='))
        opt = input('请输入功能编号：').strip()
        if opt not in func_dict or (not logged_admin and opt == '11'):
            print('此功能不存在')
            continue
        func_dict.get(opt)[1]()  # 拿到函数名加括号，执行对应功能函数
