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
from db import db_handler
from datetime import datetime
from conf import setting


# 充值接口
def recharge_interface(username, amount):
    # 获取用户数据
    user_data = db_handler.select_data(username)
    if not user_data:
        return True, f'\n用户username不存在！'
    # 给user_data里的balance充值操作
    user_data['balance'] += amount
    # 记录流水
    msg = f'\n{datetime.now()} 用户{username}充值{amount}成功，' \
          f'当前余额为：{user_data.get("balance")}元。'
    user_data['flow'].append(msg)
    # 调用数据处理层，保存修改后的user_data数据
    db_handler.save(user_data)
    return True, msg


# 提现接口
def withdraw_interface(username, amount):
    # 获取用户数据
    user_data = db_handler.select_data(username)
    balance = user_data.get('balance')
    # 计算手续费，并判断用户余额是否充足
    service_fee = setting.RATE * amount
    if balance < (service_fee + amount):
        return False, f'\n余额不足，不能进行提现操作！'
    # 给user_data里的balance提现操作
    user_data['balance'] -= (amount + service_fee)
    # 记录流水
    msg = f'\n{datetime.now()} 用户{username}提现{amount}成功，' \
          f'手续费为：{service_fee}元。' \
          f'当前余额为：{user_data.get("balance")}元。'
    user_data['flow'].append(msg)
    # 调用数据处理层，保存修改后的user_data数据
    db_handler.save(user_data)
    return True, msg


# 查看余额接口
def check_balance_interface(username):
    user_data = db_handler.select_data(username)
    balance = user_data.get('balance')
    return True, f'用户{username}当前余额为{balance}元！'


# 转账接口
def transfer_interface(username, to_username, amount):
    # 获取两个用户的用户数据，一个加钱，一个减钱
    user_data = db_handler.select_data(username)
    to_user_data = db_handler.select_data(to_username)
    # 判断to_user_data是否存在
    if not to_user_data:
        return False, f'\n目标用户{to_username}不存在！'
    # 判断当前用户余额是否充足
    if user_data.get('balance') < amount:
        return False, f'\n当前用户{username}余额不足，不允许转账！'
    # 开始转账操作
    user_data['balance'] -= amount
    to_user_data['balance'] += amount
    # 记录转账流水
    msg = f'\n{datetime.now()} 用户{username}给用户' \
          f'{to_username}转账{amount}元成功！'
    user_data['flow'].append(msg)
    to_msg = f'\n{datetime.now()} 用户{to_username}收到用户' \
             f'{username}转账{amount}元成功！'
    to_user_data['flow'].append(to_msg)
    # 保存用户到磁盘
    db_handler.save(user_data)
    db_handler.save(to_user_data)
    # 返回数据给视图层
    return True, msg


# 查看流水接口
def check_flow_interface(username):
    user_data = db_handler.select_data(username)
    flow_list = user_data.get('flow')
    return True, flow_list


# 银行支付接口
def pay_interface(username, total):
    # 拿到用户数据
    user_data = db_handler.select_data(username)

    # 判断用户余额是否充足
    if user_data.get('balance') < total:
        return False, f'\n用户{username}余额不足，支付{total}元失败！'
    # 正常支付
    user_data['balance'] -= total
    # 记录流水
    msg = f'\n{datetime.now()} 用户{username} 共消费 {total}元！' \
          f'当前余额为{user_data.get("balance")}'
    user_data['flow'].append(msg)
    # 保存用户数据
    db_handler.save(user_data)
    # 返回结果
    return True, msg

