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
        self.__map_cache__ = dict()
        for ind, var in enumerate(reversed(con.vars)):
            if self.__map_cache__.get(var, None) is None:
                self.__map_cache__[var] = code_len
            is_skip = False
            for i in range(len(con.vars) - ind, len(con.vars)):
                if con.vars[i] == var:
                    is_skip = True
                    break
            if not is_skip:
                code_len *= len(var.dom.vals_list)
        self.code_list = [0] * ((int)(code_len/32) + 1)
        self.next_set_tuple = dict()
        self.__coding_con__()
    
    def __next__vals__(self):
        rotate_over = dict()
        for var in reversed(self.con.vars):
            tmp = var.dom.vals_list
            if var.val == tmp[-1] and not rotate_over.get(var, False):
                var.val = tmp[0]
                rotate_over[var] = True
                continue
            elif rotate_over.get(var, False):
                continue
            else:
                var.val = tmp[tmp.index(var.val)+1]
                return True
        return False

    def __coding_con__(self):
        pos = 1
        last_set_tuple = -1
        while True:
            if self.con.is_sat():
                self.set_true(pos)
                self.next_set_tuple[last_set_tuple] = pos
                last_set_tuple = pos
            if self.__next__vals__():
                pos += 1
            else:
                break
        self.next_set_tuple[last_set_tuple] = -1

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
        valinds = [-1]*len(self.con.vars)
        map_over = dict()
        for i in range(len(self.con.vars)):
            var = self.con.vars[i]
            if map_over.get(var, False):
                continue
            tmp = self.__map_cache__[var]
            val_ind = (int)(pre_num/self.__map_cache__[var])
            if val_ind < len(var.dom.vals_list):
                valinds[i] = val_ind
                for j in range(len(self.con.vars)):
                    if j!= i and self.con.vars[j] == var:
                        valinds[j] = val_ind
                        map_over[var] = True
                pre_num %= self.__map_cache__[var]
        return valinds



# v1 = Variable(1, Domain([1, 2, 3]))
# v2 = Variable(1, Domain([1, 2]))

# c1 = Constraint('? + ? + ? > 3', [v2, v1, v1])

# cc = ConstraintCoder(c1)
# print(cc.get_valinds_from_code(6))

