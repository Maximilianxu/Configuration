# -*- coding: utf-8 -*-

class Domain:
    # 初始化一个定义域只需要取值集合
    def __init__(self, vals_list):
        self.vals = vals_list
        self.__valid = [True]*len(vals_list)
    
    # 给定值下标，返回该值是否有效
    def is_valid(self, val_ind):
        return self.__valid[val_ind]

    # 反转值的有效性 true->false, false->true
    def reverse(self, val_ind):
        self.__valid[val_ind] = not self.__valid[val_ind]
    
