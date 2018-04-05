# -*- coding: utf-8 -*-
# mac算法
# 目前的可优化部分：
# 1. self.vars.index(var)可以用variable_cdr来实现，用id做index，避免查询
# 2. seek_support的部分，总是set_false之后再set_true回来，思考其他方法
# 3. 回溯部分的优化，已赋值变量相关的元组可以不用添加到栈里面
# 4. 残余支持查询，提供哈希函数
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
    

    def search_solution(self):
        return self.__solve__(0)

    
    def __next_var__(self, lev):
        # 这里需要用variable_coder才能快速实现，现在缺少id
        # for var_ind, var_cdr in enumerate(self.vars):
        #     if not self.is_assigned[var_ind]:
        #         return var_ind
        # return -1  
        return lev

    # gac3rm算法
    def __mac__(self, cur_var):
        for con_cdr in self.con_cdrs:
            if cur_var in con_cdr.con.vars:
                for var in con_cdr.con.vars:
                    if (var is not cur_var) and (not self.is_assigned[self.vars.index(var)]):
                        self.queue.add((con_cdr, var))
        while len(self.queue)>0:
            cur_con_cdr, var = self.queue.pop()
            if self.__revise__(cur_con_cdr, var):
                if var.dom.dom_size() == 0:
                    return False
                for con_cdr in self.con_cdrs:
                    con_vars = con_cdr.con.vars
                    if len(con_vars) > 0 and cur_var in con_vars\
                        and (con_cdr is not cur_con_cdr):
                        for var in con_vars:
                            if var is not cur_var:
                                self.queue.add((con_cdr, var))
        return True

    def __seek_support__(self, con_cdr, cur_var, val_ind, end_point = 0xFFFFFFFF):
        cur_var_ind = con_cdr.con.vars.index(cur_var)
        tup = con_cdr.get_last_set(end_point)
        tup_dels = []
        while tup != -1:
            valinds = con_cdr.get_valinds_from_code(tup)
            if valinds[cur_var_ind] == val_ind:
                if con_cdr.is_valid_tuple(tup):
                    break
            con_cdr.set_false(tup)
            tup_dels.append(tup)
            tup = con_cdr.get_last_set(tup)
        for del_tup in tup_dels:
            con_cdr.set_true(del_tup)    
        return tup   


    def __revise__(self, con_cdr, cur_var):
        dom_size = cur_var.dom.dom_size()
        for val_ind in range(len(cur_var.dom.vals_list)):
            if not cur_var.dom.is_valid(val_ind):
                continue
            pos = self.supp.get((con_cdr, cur_var, val_ind), None)
            if pos is not None and con_cdr.is_valid_tuple(pos) :
                continue
            tup = self.__seek_support__(con_cdr, cur_var, val_ind)
            if tup is -1:
                cur_var.dom.set_invalid(val_ind)
                self.del_vals[-1].append((cur_var, val_ind))
            else:
                for (prop_var, prop_valind) in zip(con_cdr.con.vars, con_cdr.get_valinds_from_code(tup)):
                    self.supp[(con_cdr, prop_var, prop_valind)] = tup
            
        return dom_size != cur_var.dom.dom_size()

    def __assign_val__(self, var, val_ind):
        for ind in range(len(var.dom.vals_list)):
            if ind != val_ind:
                var.dom.set_invalid(ind)
                self.del_vals[-1].append((var, ind))
    
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
                self.__assign_val__(cur_var, val_ind)
                rslt = self.__mac__(cur_var)
                if rslt and self.__solve__(lev + 1):
                    self.is_assigned[cur_var_ind] = False
                    is_solvable = True
                    if self.sol_num >= self.MAX_SOLS_NUM:
                        return is_solvable
                self.__trace_back__(self.del_vals.pop())
        return is_solvable


v1 = Variable(1, Domain([1, 2, 3]))
v2 = Variable(1, Domain([1, 2, 3]))
v3 = Variable(1, Domain([1, 2, 3]))
# 'x < y <= z'
c1 = Constraint('? < ? <= ?', [v1, v2, v3])
task = Task([v1, v2, v3], [c1])
solver = Solver(task)
is_solvable = solver.search_solution()
# print(is_solvable)
sols = solver.rslt.solutions
for sol in sols:
    print(sol.vals_list)
                    
