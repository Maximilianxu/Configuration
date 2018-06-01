# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, session, jsonify
import datetime
from Configuration.inventory.component_inv import find_subcomponents_id_name
from Configuration.inventory.order_inv import find_all_orders_by_email, insert_order
from Configuration.inventory.product_inv import find_all_constraints_by_product_id, find_all_properties_by_product_id
from Configuration.inventory.property_inv import find_all_propertys
from Configuration.inventory.constraint_inv import add_constraint, find_a_constraint, delete_constraint
from Configuration.inventory.con_include_p_inv import add_relation, find_constraints_id_by_property, delete_relation_by_constraint
from Configuration.model.order import Order
from Configuration.model.task import Task
from Configuration.model.constraint import Constraint
from Configuration.solver.solver import Solver

constraint_manager = Blueprint('constraint_manager', __name__, template_folder='templates')

@constraint_manager.route('/constraint')
def constraint():
    model_name = session['model_name']
    root_component_id = session['root_component_id']
    root_component_name = session['root_component_name']
    subcomponents = find_subcomponents_id_name(root_component_id)
    return render_template('constraint.html', model_name=model_name,\
            root_component_id=root_component_id, root_component_name=root_component_name,\
            subcomponents=subcomponents)

@constraint_manager.route('/constraint/add', methods=['POST'])
def add_new_constraint():
    model_id = session['model_id']
    data = request.get_json()
    expression = data['cons_expr']
    expression_display = data['expr_display']
    property_ids = data['vars']
    constraint_id = add_constraint(model_id, expression, expression_display)
    add_relation(constraint_id, property_ids)
    return jsonify(constraint_id)

@constraint_manager.route('/constraint/item', methods=['POST'])
def find_properties_constraints_of_component():
    comp_id = request.get_json()['id']
    propertys = find_all_propertys(comp_id)
    constraints_id = []
    for property in propertys:
        constraints_id += find_constraints_id_by_property(property.id)
    propertys_json = [property.toJSON() for property in propertys]
    new_constraints_id = list(set(constraints_id))
    new_constraints_id.sort()
    constraints = []
    for constraint_id in new_constraints_id:
        constraint = find_a_constraint(constraint_id)
        constraints.append(constraint)
    result = {'propertys': propertys_json, 'constraints': constraints}
    return jsonify(result)

@constraint_manager.route('/constraint/delete', methods=['POST'])
def delete_a_constraint():
    data = request.get_json()
    cons_id = data['id']
    delete_constraint(cons_id)
    delete_relation_by_constraint(cons_id)
    return 'success'

@constraint_manager.route('/constraint/check', methods=['POST'])
def check_constraints():
    prod_id = session['model_id']
    variables = find_all_properties_by_product_id(prod_id)
    cons_tuple = find_all_constraints_by_product_id(prod_id, variables)
    cons = cons_tuple[0]
    expressions_display = cons_tuple[1]
    task = Task(variables, cons)
    properties = task.vars
    solver = Solver(task)
    solvable = solver.search_solution()
    rslt = solver.rslt
    solution = 'S'
    if solvable:
        for sol in rslt.solutions:
            for var_ind, val in enumerate(sol.vals_list):
                cur_var = properties[var_ind]
                solution += (cur_var.name + ' = '+ \
                cur_var.domin_display[cur_var.dom.vals_list.index(val)] + cur_var.dataunit + ' ')
            solution += ';'
        return solution
    conflict = 'C'
    if not solvable:
        conf_cons = solver.compute_explanation()
        for con in conf_cons:
            con_index = cons.index(con)
            conflict += (expressions_display[con_index] + ';')
        return conflict
