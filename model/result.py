# -*- coding: utf-8 -*-

# 保存求解结果

class Solution:

    # vals_list存放变量取值的列表
    def __init__(self, vals_list):
        self.vals_list = vals_list

class Explanation:

    # expl_cons存放最小冲突约束集合
    def __init__(self, expl_cons):
        self.expl_cons = expl_cons

class Result:

    def __init__(self, solutions, explanation):
        self.solutions = solutions
        self.explanation = explanation