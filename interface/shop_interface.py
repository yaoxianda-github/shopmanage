#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : shop_interface.py
@Date    : 2025/5/28 10:35
@Author  : yaoxianda
@Version : 1.0
@Contact : 2386339350@qq.com
@License : (C) Copyright 2024-2024, yaoxianda.
@Desc    : What this script does.
购物相关接口

"""

from db import db_handler
from interface import bank_interface


# 查询商品信息接口
def check_goods_interface(goods_filename):
    goods = db_handler.select_data(goods_filename, is_user=False)
    return goods


# 添加购物车接口
def add_shop_cart_interface(username, shopping_cart):
    # 获取用户数据里的购物车数据
    user_data = db_handler.select_data(username)
    shopping_cart_file = user_data.get('shopping_cart', {})  # 不存在则默认空字典  # 如果需要修改值，就用中括号进行取值，否则可以用get方法进行获取字典的值
    # 添加购物车
    for name in shopping_cart.keys():
        if name in shopping_cart_file:
            shopping_cart_file[name]['数量'] += shopping_cart.get('name').get('数量')
        else:
            shopping_cart_file[name] = shopping_cart[
                name]  # shopping_cart.get('name') 中 'name' 是字符串字面量，而非循环变量 name ，会导致始终取 shopping_cart 里 'name' 键的值（实际不存在，返回 None ），最终把 None 赋值给 shopping_cart_file[name]
    # 保存用户数据
    db_handler.save(user_data)
    # 给用户视图层返回数据
    return True, '\n购物车添加成功！'


# 结算接口
def close_account_interface(username, shopping_cart):
    # 计算商品总金额
    total = 0
    for good_info in shopping_cart.values():
        price = good_info.get('price')
        num = good_info.get('数量')
        total += (price * num)
    flag, msg = bank_interface.pay_interface(username, total)
    return flag, msg, total  # 把结果返回给视图层


# 查看购物车接口
def check_shop_cart_interface(username):
    user_data = db_handler.select_data(username)
    shop_cart_file = user_data['shopping_cart']
    return shop_cart_file

# 清空购物车接口
def clear_shop_cart_interface(username):
    user_data = db_handler.select_data(username)
    user_data['shopping_cart'] = {}
    db_handler.save(user_data)