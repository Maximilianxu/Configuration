# -*- coding: utf-8 -*-

class Constraint:

    # expr是有效的python逻辑表达式
    # expr应当为以下形式（由于去掉了id属性）：每一个变量以特殊字符作为占位符，
    # 顺序为vars列表顺序
    # 比如expr: ? < ?, vars: [A, B]，即表示约束A.val<B.val
    def __init__(self, expr, vars):
        self.expr = expr
        self.vars = vars
    
    # 约束是否满足
    def is_sat(self):
        tmp_expr = (self.expr + '.')[:-1]
        var_ind = 0
        for ind, ch in enumerate(tmp_expr):
            if ch == '?':
                tmp_expr = tmp_expr[:ind] + str(self.vars[var_ind].val) + tmp_expr[ind+1:]
                var_ind += 1
        return eval(tmp_expr)

