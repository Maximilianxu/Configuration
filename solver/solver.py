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
        self.is_solvable = False
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
        self.del_vals.append([])
        solvable = self.__solve__(0)
        self.__end_solve__()
        return solvable
    
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

    # 回复状态
    def __end_solve__(self):
        self.supp.clear()
        self.del_vals.clear()
        for var in self.vars:
            var.val = var.dom.vals_list[0]

    def __solve__(self, lev):
        if lev == len(self.vars):
            self.sol_num += 1
            vals_list = []
            for var in self.vars:
                vals_list.append(var.val)
            sol = Solution(vals_list)
            self.rslt.solutions.append(sol)
            self.is_solvable = True
            return True    
        cur_var_ind = self.__next_var__(lev)
        cur_var = self.vars[cur_var_ind]
        cur_dom = cur_var.dom
        solvable = False
        for val_ind, val in enumerate(cur_dom.vals_list):
            if cur_dom.is_valid(val_ind):
                cur_var.val = val
                self.is_assigned[cur_var_ind] = True
                self.del_vals.append([])  
                if self.__mac__(cur_var) and self.__solve__(lev + 1):
                    solvable = True
                    if self.sol_num >= self.MAX_SOLS_NUM:
                        self.is_assigned[cur_var_ind] = False
                        self.__trace_back__(self.del_vals.pop())
                        return solvable
                self.is_assigned[cur_var_ind] = False
                self.__trace_back__(self.del_vals.pop())  
        return solvable
    
    def __is_consistent__(self, con_cdrs):
        pre_con_cdrs = self.con_cdrs
        explain_con_cdrs = []
        self.con_cdrs = explain_con_cdrs
        pre_max_sols_num = self.MAX_SOLS_NUM
        self.MAX_SOLS_NUM = 1
        is_consistent = self.search_solution()
        self.MAX_SOLS_NUM = pre_max_sols_num
        self.con_cdrs = pre_con_cdrs
        return is_consistent

    # cons均为Constraint的列表
    def __quickxplain__(self, basic_cons, delta_cons, custom_cons):
        if len(delta_cons) > 0 and not self.__is_consistent__(basic_cons):
            return []
        if len(custom_cons) == 1:
            return custom_cons
        splt_k = (int)(len(custom_cons) / 2)
        C1 = custom_cons[:splt_k]
        C2 = custom_cons[splt_k:]
        delta2 = self.__quickxplain__(basic_cons+C1, C1, C2)
        delta1 = self.__quickxplain__(basic_cons+delta2, delta2, C1)
        return delta1 + delta2

    def __quick_explain__(self, basic_cons, custom_cons):
        if self.is_solvable or len(custom_cons) == 0:
            return []
        con_cdrs = self.__quickxplain__(basic_cons, basic_cons, custom_cons)
        return list(map(lambda x: x.con, con_cdrs))
    
    # 模型检测时，不用给参数即可; 否则，第一个参数意即self.con_cdrs列表中，start之前的为basic_cons
    def compute_explanation(self, custom_cons_start = 0):
        return self.__quick_explain__(self.con_cdrs[:custom_cons_start], self.con_cdrs[custom_cons_start:])



v1 = Variable(1, Domain([1, 2, 3]))
v2 = Variable(1, Domain([1, 2, 3]))
v3 = Variable(2, Domain([2, 3, 4]))
# 'x < y <= z'
# bug here
c1 = Constraint('? < ? <= ?', [v1, v2, v3])
c2 = Constraint('? >= ?', [v1, v2])
task = Task([v1, v2, v3], [c1, c2])
solver = Solver(task)

is_solvable = solver.search_solution()
print('====> has any solutions? ', is_solvable)
sols = solver.rslt.solutions
for sol in sols:
    print(sol.vals_list)

if not is_solvable:
    print('====> the conflict constraints including:')
    rslt = solver.compute_explanation()
    for ind, con in enumerate(rslt):
        print(str(ind+1)+'. '+con.expr)

print('====================')
                    
