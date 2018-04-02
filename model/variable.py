# -*- coding: utf-8 -*-

class Variable:
    # 变量取值（初始化一个默认值）以及定义域
    def __init__(self, val, dom):
        self.val = val
        self.dom = dom
    
    def is_valid(self, val_ind):
        return self.dom.is_valid(val_ind)
    
