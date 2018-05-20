# -*- coding: utf-8 -*-
from flask import Blueprint,  request, jsonify, session
from Configuration.inventory.property_inv import add_property, update_property, find_properties_id_name,\
        find_a_property, delete_property
from Configuration.inventory.constraint_inv import delete_constraint
from Configuration.inventory.con_include_p_inv import find_constraints_id_by_property,\
        delete_relation_by_constraint
from Configuration.model.property import Property

property_manager = Blueprint('property_manager', __name__, template_folder='templates')

@property_manager.route('/property/item', methods=['POST'])
def find_property_by_id():
    data = request.get_json()
    property = find_a_property(data['id'])
    return jsonify(property)

@property_manager.route('/property/create', methods=['POST'])
def create_property():
    data = request.get_json()
    datatype = data['datatype']
    domin_display = data['domin_display']
    if(datatype == 'string'):
        display_list = domin_display.split(',')
        vars_list = range(len(display_list))
        vars_str_list = [str(i) for i in vars_list]
        domin = ','.join(vars_str_list)
    else:
        domin = domin_display
    component_id = session['component_id']
    property_id = add_property(component_id, data['name'], data['introduction'], datatype, data['dataunit'], domin, domin_display)
    resp = {'id': property_id}
    return jsonify(resp)

@property_manager.route('/property/update', methods=['POST'])
def update_a_property():
    data = request.get_json()
    datatype = data['datatype']
    domin_display = data['domin_display']
    if(datatype == 'string'):
        display_list = domin_display.split(',')
        vars_list = range(len(display_list))
        vars_str_list = [str(i) for i in vars_list]
        domin = ','.join(vars_str_list)
    else:
        domin = domin_display
    print(domin)
    print(domin_display)
    update_property(data['id'], data['name'], data['introduction'], datatype, data['dataunit'], domin, domin_display)
    return 'success'

@property_manager.route('/property/delete', methods=['POST'])
def delete_a_property():
    data = request.get_json()
    property_id = data['id']
    constraints_id = find_constraints_id_by_property(property_id)
    for c_id in constraints_id:
        delete_constraint(c_id)
        delete_relation_by_constraint(c_id)
    delete_property(property_id)
    return 'success'