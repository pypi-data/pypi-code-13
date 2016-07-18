# coding=utf-8
"""递归列表"""


def test_model(datas):
    """循环datas"""
    for data in datas:
        if isinstance(data, list):
            a(data)
        else:
            print(data)