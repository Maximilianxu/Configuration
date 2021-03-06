# -*- coding: utf-8 -*-

class Variable:
    # 变量取值（初始化一个默认值）以及定义域
    def __init__(self, val, dom):
        self.val = val
        self.dom = dom
    
    # 测试某个值是否有效
    def is_valid(self, val_ind):
        return self.dom.is_valid(val_ind)
    
    def set_valid(self, val_ind):
        self.dom.set_valid(val_ind)
    
    def set_invalid(self, val_ind):
        self.dom.set_invalid(val_ind)
    
    def __str__(self):
        return ' '.join(['%s:%s' % item for item in self.__dict__.items()])    
