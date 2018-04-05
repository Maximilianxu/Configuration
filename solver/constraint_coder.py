# -*- coding: utf-8 -*-
# 给任意约束提供比特形式的编码，以及一些基于此的函数
# 一个约束与其编码器一一对应，所以，初始阶段，Solver将约束进行编码
import sys
sys.path.append("../")

from Configuration.model.constraint import Constraint
from Configuration.model.variable import Variable
from Configuration.model.domain import Domain

class ConstraintCoder:

    __ALLF__ = 0xFFFFFFFF
    __LOOKUP__ = [0, 1, 28, 2, 29, 14, 24, 3,\
    30, 22, 20, 15, 25, 17, 4, 8, 31, 27, 13, 23, 21, 19,\
    16, 7, 26, 12, 18, 6, 11, 5, 10, 9]

    def __init__(self, con):
        self.con = con
        code_len = 1
        self.__map_cache__ = [1] * len(con.vars)
        for ind, var in enumerate(reversed(con.vars)):
            self.__map_cache__[len(con.vars)-ind-1] = code_len
            code_len *= len(var.dom.vals_list)
        self.code_list = [0] * ((int)(code_len/32) + 1)
        self.__coding_con__()
    
    def __next__vals__(self):
        for var in reversed(self.con.vars):
            tmp = var.dom.vals_list
            if var.val == tmp[-1]:
                var.val = tmp[0]
                continue
            else:
                var.val = tmp[tmp.index(var.val)+1]
                return True
        return False

    def __coding_con__(self):
        ind = 1
        while True:
            if self.con.is_sat():
                self.set_true(ind)
            if self.__next__vals__():
                ind += 1
            else:
                break

    def set_true(self, pos):
        ind = (int)(pos / 32)
        ofst = pos % 32
        if ofst == 0:
            ofst = 32
        self.code_list[ind] = (self.code_list[ind] | (1<<(32-ofst))) & self.__ALLF__

    def set_false(self, pos):
        ind = (int)(pos / 32)
        ofst = pos % 32
        if ofst == 0:
            ofst = 32
        self.code_list[ind] = (self.code_list[ind] & (~(1<<(32-ofst)))) & self.__ALLF__

    def get_value(self, pos):
        ind = (int)(pos / 32)
        ofst = pos % 32
        if ofst == 0:
            ofst = 32
        mask = (~(1 << (32-ofst))) & self.__ALLF__
        return (self.code_list[ind] | mask) != mask
    

    def get_last_set(self, start_pos = 0xFFFFFFFF):
        start_ind = int(start_pos / 32)
        start_ind = min(len(self.code_list)-1, start_ind)
        for i in range(start_ind, -1, -1):
            cur_code = self.code_list[i]
            tmp = (cur_code&(-cur_code)).bit_length()-1
            if tmp != -1:
                return (i+1) * 32 - tmp
        return -1
    
    def get_first_set(self, start_pos = 0):
        start_ind = int(start_pos / 32)
        for i in range(start_ind, len(self.code_list)):
            cur_code = self.code_list[i]
            if cur_code == 0:
                continue
            cur_code |= cur_code >> 1
            cur_code |= cur_code >> 2
            cur_code |= cur_code >> 4
            cur_code |= cur_code >> 8
            cur_code |= cur_code >> 16
            cur_code = (cur_code >> 1) + 1
            return (i+1)*32-self.__LOOKUP__[((cur_code*0x077CB531)&self.__ALLF__)>>27]
        return -1
    
    # 从二级制编码位置获取值下标的元组
    def get_valinds_from_code(self, pos):
        pre_num = pos - 1
        valinds = []
        for i in range(len(self.con.vars)):
            tmp = self.__map_cache__[i]
            val_ind = (int)(pre_num/self.__map_cache__[i])
            valinds.append(val_ind)
            pre_num %= self.__map_cache__[i]
        return valinds
    
    # 元组是否有效，即元组的各个成分是否为有效值
    def is_valid_tuple(self, pos, valinds=None):
        if valinds == None:
            valinds = self.get_valinds_from_code(pos)
        is_valid = True
        for ind, val_ind in enumerate(valinds):
            if not self.con.vars[ind].is_valid(val_ind):
                is_valid = False
                break
        return is_valid


'''
v1 = Variable(1, Domain([1, 2, 3]))
v2 = Variable(1, Domain([1, 2, 3]))
v3 = Variable(1, Domain([1, 2, 3]))

c1 = Constraint('? < ? <= ?', [v1, v2, v3])

cc = ConstraintCoder(c1)
print(cc.get_last_set())
print(cc.get_first_set())
print(cc.get_last_set(19))
print(cc.get_value(4), cc.get_value(5))
cc.set_false(5)
print(cc.get_first_set())
cc.set_true(19)
print(cc.get_last_set())
print(cc.get_vals_from_code(5))
'''
