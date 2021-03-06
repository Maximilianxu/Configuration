# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify, session
from queue import Queue
from Configuration.inventory.component_inv import add_component, find_a_component, find_subcomponents_id_name, \
    update_component, delete_component
from Configuration.inventory.property_inv import find_properties_id_name, delete_all_propertys, find_all_propertys
from Configuration.inventory.constraint_inv import delete_constraint
from Configuration.inventory.con_include_p_inv import find_constraints_id_by_property,\
    delete_relation_by_constraint
from Configuration.model.component import Component

component_manager = Blueprint('component_manager', __name__, template_folder='templates')

@component_manager.route('/component/item', methods=['POST'])
def find_component_by_id():
    data = request.get_json()
    component_id = data['id']
    session['component_id'] = component_id
    component = find_a_component(component_id)
    properties = find_properties_id_name(component_id)
    component['properties'] = properties
    return jsonify(component)

@component_manager.route('/component/subcomponents', methods=['POST'])
def find_subcomponents():
    data = request.get_json()
    father_component_id = data['id']
    subcomponents = find_subcomponents_id_name(father_component_id)
    return jsonify(subcomponents)

@component_manager.route('/component/add', methods=['POST'])
def create_component():
    data = request.get_json()
    model_id = session['model_id']
    component = Component(0, data['father_component_id'], data['name'], data['introduction'])
    component.id = add_component(model_id, component)
    resp = {'id': component.id}
    return jsonify(resp)

@component_manager.route('/component/update', methods=['POST'])
def update_a_component():
    data = request.get_json()
    update_component(data['id'], data['name'], data['introduction'])
    return 'success'

@component_manager.route('/component/delete', methods=['POST'])
def delete_components_by_father_id():
    q = Queue()
    data = request.get_json()
    q.put(data['id'])
    while not q.empty():
        component_id = q.get()
        subcoms = find_subcomponents_id_name(component_id)
        for sub in subcoms:
            q.put(sub['id'])
        properties = find_properties_id_name(component_id)
        for pro in properties:
            constraints_id = find_constraints_id_by_property(pro['id'])
            for c_id in constraints_id:
                delete_constraint(c_id)
                delete_relation_by_constraint(c_id)
        delete_all_propertys(component_id)
        delete_component(component_id)
    return 'success'

@component_manager.route('/component/properties', methods=['POST'])
def find_properties_by_comp_id():
    import json
    comp_id = request.get_json()['id']
    props = find_all_propertys(comp_id)
    props_json = json.dumps([prop.toJSON() for prop in props])
    return props_json

