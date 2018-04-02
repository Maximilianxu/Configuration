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
        for var in self.vars:
            tmp_expr.replace('?', str(var.val), 1)
        return eval(tmp_expr)

