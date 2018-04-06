# -*- coding: utf-8 -*-
# mac算法
# 目前的可优化部分：

import sys
sys.path.append("../")

from Configuration.model.result import Solution, Explanation, Result
from Configuration.model.constraint import Constraint
from Configuration.model.variable import Variable
from Configuration.model.domain import Domain
from Configuration.model.task import Task

from constraint_coder import ConstraintCoder

class Solver:

    # 限制解的最多数量，防止求解时间过长
    MAX_SOLS_NUM = 10

    def __init__(self, task):
        self.vars = task.vars
        self.con_cdrs = []
        for con in task.cons:
            self.con_cdrs.append(ConstraintCoder(con))     
        self.rslt = Result([], None)
        # 变量是否已被赋值
        self.is_assigned = [False] * len(self.vars)
        # 启发式
        self.wdegs = [1] * len(self.vars)
        # 记录删除的值列表（元素为被删除的值列表列表），用于回溯,
        self.del_vals = []
        # 记录解的数量
        self.sol_num = 0
        # 残余支持
        self.supp = dict()
        # 传播队列
        self.queue = set()
        # 变量与其下标映射
        self.var_ind_map = dict()
        for var_ind, var in enumerate(self.vars):
            self.var_ind_map[var] = var_ind  

    def search_solution(self):
        return self.__solve__(0)
    
    def __next_var__(self, lev):
        min_dom_wdeg = 0xFFFFFFFF
        next_var_ind = -1
        for ind, assigned in enumerate(self.is_assigned):
            if assigned:
                continue
            tmp = self.vars[ind].dom.dom_size()/self.wdegs[ind]
            if tmp < min_dom_wdeg:
                min_dom_wdeg = tmp
                next_var_ind = ind
        return next_var_ind

    # 一个基本操作
    def __prop_operations__(self, cur_var, cur_con_cdr = None, add_queue = True):
        for con_cdr in self.con_cdrs:
            con_vars = con_cdr.con.vars
            if len(con_vars) > 0 and cur_var in con_vars and (con_cdr is not cur_con_cdr):
                for var in con_vars:
                    var_ind = self.var_ind_map[var]
                    if (var is not cur_var) and (not self.is_assigned[var_ind]):
                        if add_queue:
                            self.queue.add((con_cdr, var))
                        else:
                            self.wdegs[var_ind] += 1

        # 元组是否有效，即元组的各个成分是否为有效值
    def is_valid_tuple(self, con_cdr, valinds):
        is_valid = True
        for ind, val_ind in enumerate(valinds):
            cur_var = con_cdr.con.vars[ind]
            if not cur_var.is_valid(val_ind) or \
                (self.is_assigned[self.var_ind_map[cur_var]] and \
                cur_var.val != cur_var.dom.vals_list[val_ind]):

                is_valid = False
                break

        return is_valid

    # gac3rm算法
    def __mac__(self, cur_var):
        self.__prop_operations__(cur_var)
        while len(self.queue)>0:
            cur_con_cdr, var = self.queue.pop()
            if self.__revise__(cur_con_cdr, var):
                if var.dom.dom_size() == 0:
                    self.__prop_operations__(cur_var, add_queue=False)
                    return False
                self.__prop_operations__(var, cur_con_cdr=cur_con_cdr)           
        return True

    def __seek_support__(self, con_cdr, cur_var, val_ind):
        cur_var_ind = self.var_ind_map[cur_var]
        pos = -1
        while True:
            pos = con_cdr.next_set_tuple.get(pos, -1)
            if pos == -1:
                return pos
            valinds = con_cdr.get_valinds_from_code(pos)
            if con_cdr.get_value(pos) and \
                valinds[cur_var_ind] == val_ind and \
                self.is_valid_tuple(con_cdr, valinds):
                    return pos
        return -1

    def __revise__(self, con_cdr, cur_var):
        dom_size = cur_var.dom.dom_size()
        for val_ind in range(len(cur_var.dom.vals_list)):
            if not cur_var.is_valid(val_ind):
                continue
            pos = self.supp.get((con_cdr, cur_var, val_ind), None)
            if pos is not None:
                valinds = con_cdr.get_valinds_from_code(pos)
                if self.is_valid_tuple(con_cdr, valinds):
                    continue
            tup = self.__seek_support__(con_cdr, cur_var, val_ind)
            if tup is -1:
                cur_var.dom.set_invalid(val_ind)
                self.del_vals[-1].append((cur_var, val_ind))
            else:
                for (prop_var, prop_valind) in zip(con_cdr.con.vars, con_cdr.get_valinds_from_code(tup)):
                    self.supp[(con_cdr, prop_var, prop_valind)] = tup
            
        return dom_size != cur_var.dom.dom_size()
    
    def __trace_back__(self, cur_del_vals):
        while len(cur_del_vals) > 0:
            var, val_ind = cur_del_vals.pop()
            var.dom.set_valid(val_ind)

    def __solve__(self, lev):
        if lev == len(self.vars):
            self.sol_num += 1
            vals_list = []
            for var in self.vars:
                vals_list.append(var.val)
            sol = Solution(vals_list)
            self.rslt.solutions.append(sol)
            return True    
        cur_var_ind = self.__next_var__(lev)
        cur_var = self.vars[cur_var_ind]
        cur_dom = cur_var.dom
        is_solvable = False
        for val_ind, val in enumerate(cur_dom.vals_list):
            if cur_dom.is_valid(val_ind):
                cur_var.val = val
                self.is_assigned[cur_var_ind] = True
                self.del_vals.append([])  
                if self.__mac__(cur_var) and self.__solve__(lev + 1):
                    self.is_assigned[cur_var_ind] = False
                    is_solvable = True
                    if self.sol_num >= self.MAX_SOLS_NUM:
                        return is_solvable
                self.__trace_back__(self.del_vals.pop())
        return is_solvable


v1 = Variable(1, Domain([1, 2, 3]))
v2 = Variable(1, Domain([1, 2, 3]))
v3 = Variable(2, Domain([2, 3, 4]))
# 'x < y <= z'
c1 = Constraint('? < ? <= ?', [v1, v2, v3])
task = Task([v1, v2, v3], [c1])
solver = Solver(task)
is_solvable = solver.search_solution()
# print(is_solvable)
sols = solver.rslt.solutions
for sol in sols:
    print(sol.vals_list)
                    
