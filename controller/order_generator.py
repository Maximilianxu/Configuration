# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, session, jsonify
import datetime
from Configuration.inventory.component_inv import find_subcomponents_id_name
from Configuration.inventory.order_inv import find_all_orders_by_email, insert_order
from Configuration.inventory.product_inv import find_all_constraints_by_product_id, find_all_properties_by_product_id
from Configuration.inventory.property_inv import find_all_propertys
from Configuration.model.order import Order
from Configuration.model.task import Task
from Configuration.model.constraint import Constraint
from Configuration.solver.solver import Solver
order_generator = Blueprint('order_generator', __name__, template_folder='templates')

@order_generator.route('/config')
def config():
    root_component_id = session['root_component_id']
    root_component_name = session['root_component_name']
    subcomponents = find_subcomponents_id_name(root_component_id)
    return render_template('config.html',\
            root_component_id=root_component_id, root_component_name=root_component_name,\
            subcomponents=subcomponents)

@order_generator.route('/order')
def order():
    user_email = session['user_email']
    orders = find_all_orders_by_email(user_email)
    print('====>')
    for ord in orders:
        print(ord.assignments)
    return render_template('order.html', orders = orders)

@order_generator.route('/order/reqs', methods=['POST'])
def sub_reqs():
    import json
    reqs = request.get_json()
    prod_id = session['model_id']
    cons = find_all_constraints_by_product_id(prod_id)
    variables = find_all_properties_by_product_id(prod_id)
    task = Task(variables, cons)
    properties = task.vars
    constraints = task.cons
    cons_id = len(constraints)
    for req in reqs:
        con_vars = []
        for prop_id in req['vars']:
            for prop in properties:
                if prop.id == prop_id:
                    is_exist = True
                    con_vars.append(prop)
        con = Constraint(cons_id, req['expr'], con_vars)
        task.cons.append(con)
    solver = Solver(task)
    solvable = solver.search_solution()
    rslt = solver.rslt
    solution = 'S'
    if solvable:
        for sol in rslt.solutions:
            for var_ind, val in enumerate(sol.vals_list):
                cur_var = properties[var_ind]
                solution += (cur_var.name + ' = '+ \
                cur_var.domin_display[cur_var.dom.vals_list.index(val)] + ' ')
            solution += ';'
        return solution
    conflict = 'C'
    if not solvable:
        conf_cons = solver.compute_explanation()
        var_ind = 0
        for con in conf_cons:
            expr = con.expr
            cur_var = con.vars[var_ind]
            val_display = ''
            digit_area = False
            tmp_expr = (expr + '.')[:-1]
            for ch in tmp_expr:
                tmp_ind = expr.index(ch)
                if not ch.isdigit():
                    digit_area = False
                if ch == '?':
                    val_ind = cur_var.dom.vals_list.index(cur_var.val)
                    val_display = cur_var.domin_display[val_ind]
                    expr = expr[:tmp_ind] + cur_var.name + expr[tmp_ind+1:]
                    var_ind += 1
                if digit_area:
                    expr = expr[:tmp_ind] + expr[tmp_ind+1:]
                if not digit_area and ch.isdigit():
                    digit_area = True
                    expr = expr[:tmp_ind] + val_display + expr[tmp_ind+1:]                 
            conflict += (expr+';')
        return conflict

@order_generator.route('/order/new', methods=['POST'])
def sub_order():
    # 变量赋值情况以及总价格
    data = request.get_json()
    assignments = data['assignments']
    print(assignments)
    price = data['price']
    user_email = session['user_email']
    ord = Order(user_email, session['model_id'], assignments, datetime.date.today(), price, 'up')
    insert_order(ord)
    return 'success'