# -*- coding: utf-8 -*-

class Domain:
    # 初始化一个定义域只需要取值集合
    def __init__(self, vals_list):
        self.vals_list = vals_list
        self.__valid__ = [True]*len(vals_list)
        self.__valid_size__ = len(vals_list)
    
    # 给定值下标，返回该值是否有效
    def is_valid(self, val_ind):
        return self.__valid__[val_ind]
    
    def set_valid(self, val_ind):
        if not self.__valid__[val_ind]:
            self.__valid__[val_ind] = True
            self.__valid_size__ += 1
    
    def set_invalid(self, val_ind):
        if self.__valid__[val_ind]:
            self.__valid__[val_ind] = False
            self.__valid_size__ -= 1
    
    # 返回当前有效定义域的大小
    def dom_size(self):
        return self.__valid_size__
    
