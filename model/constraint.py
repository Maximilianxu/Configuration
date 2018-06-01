# -*- coding: utf-8 -*-

class Constraint:

    # expr是有效的python逻辑表达式
    # expr应当为以下形式（由于去掉了id属性）：每一个变量以特殊字符作为占位符，
    # 顺序为vars列表顺序
    # 比如expr: ? < ?, vars: [A, B]，即表示约束A.val<B.val
    def __init__(self, id, expr, vars):
        self.id = id
        self.expr = expr
        self.vars = vars
    
    # 约束是否满足
    def is_sat(self):
        tmp_expr = (self.expr + '.')[:-1]
        var_ind = 0
        while var_ind < len(self.vars):
            tmp_expr = tmp_expr.replace('?', str(self.vars[var_ind].val), 1)
            var_ind += 1
        return eval(tmp_expr)

    def __str__(self):
        return ' '.join(['%s:%s' % item for item in self.__dict__.items()]) + ' ' + ' '.join(str(item) for item in self.vars)
