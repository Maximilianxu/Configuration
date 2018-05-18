# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, jsonify, flash, session
from queue import Queue
from Configuration.inventory.component_inv import add_component, find_a_component, find_subcomponents_id_name, \
    update_component, delete_component
from Configuration.inventory.property_inv import find_properties_id, delete_all_propertys
from Configuration.inventory.constraint_inv import delete_constraint
from Configuration.inventory.con_include_p_inv import find_constraints_id_by_property,\
    delete_relation_by_constraint
from Configuration.model.component import Component

component_creator = Blueprint('component_creator', __name__, template_folder='templates')

@component_creator.route('/component')
def component():
    root_component_id = session['root_component_id']
    root_component_name = session['root_component_name']
    subcomponents = find_subcomponents_id_name(root_component_id)
    return render_template('m_component.html',\
            root_component_id=root_component_id, root_component_name=root_component_name,\
            subcomponents=subcomponents)

@component_creator.route('/component/item', methods=['POST'])
def find_model_by_id():
    data = request.get_json()
    component = find_a_component(data['id'])
    return jsonify(component)

@component_creator.route('/component/subcomponents', methods=['POST'])
def find_subcomponents():
    data = request.get_json()
    father_component_id = data['id']
    subcomponents = find_subcomponents_id_name(father_component_id)
    return jsonify(subcomponents)

@component_creator.route('/component/add', methods=['POST'])
def create_component():
    data = request.get_json()
    model_id = session['model_id']
    component = Component(0, data['father_component_id'], data['name'], data['introduction'])
    component.id = add_component(model_id, component)
    resp = {'id': component.id}
    return jsonify(resp)

@component_creator.route('/component/update', methods=['POST'])
def update_a_component():
    data = request.get_json()
    update_component(data['id'], data['name'], data['introduction'])
    flash('Update component success!')
    return 'success'

@component_creator.route('/component/delete', methods=['POST'])
def delete_components_by_father_id():
    q = Queue()
    data = request.get_json()
    q.put(data['id'])
    while not q.empty():
        component_id = q.get()
        subcoms = find_subcomponents_id_name(component_id)
        for sub in subcoms:
            q.put(sub['id'])
        properties_id = find_properties_id(component_id)
        for p_id in properties_id:
            constraints_id = find_constraints_id_by_property(p_id)
            for c_id in constraints_id:
                delete_constraint(c_id)
                delete_relation_by_constraint(c_id)
        delete_all_propertys(component_id)
        delete_component(component_id)
    return 'success'

