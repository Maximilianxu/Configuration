# -*- coding: utf-8 -*-
import datetime
from flask import Blueprint, render_template, request, session, jsonify, flash
from Configuration.inventory.product_inv import find_models_id_name, find_a_model,\
        add_product, delete_product, update_root_component_id, update_product,\
        update_realease, update_deadline        
from Configuration.inventory.component_inv import add_component, delete_all_components, find_components_id
from Configuration.inventory.property_inv import delete_all_propertys
from Configuration.inventory.constraint_inv import delete_all_constraints, find_constraints_id
from Configuration.inventory.con_include_p_inv import delete_constraint
from Configuration.model.product import Product
from Configuration.model.component import Component

model_creator = Blueprint('model_creator', __name__, template_folder='templates')

@model_creator.route('/model')
def model():
    user_email = session['user_email']
    models = find_models_id_name(user_email)
    return render_template('model.html', models=models)

@model_creator.route('/model/item', methods=['POST'])
def find_model_by_id():
    data = request.get_json()
    mod = find_a_model(data['id'])
    return jsonify(mod)

@model_creator.route('/model/create', methods=['POST'])
def create_model():
    data = request.get_json()
    user_email = session['user_email']
    model = Product(0, data['name'], data['introduction'], 0, datetime.datetime.now(), 0)
    model.id = add_product(user_email, model)
    component = Component(0, 0, data['name'], data['introduction'])
    component.id = add_component(model.id, component)
    update_root_component_id(model.id, component.id)
    flash('Create model success!')
    return 'success'

@model_creator.route('/model/release', methods=['POST'])
def release_model():
    data = request.get_json()
    model_id = data['id']
    update_realease(model_id)
    update_deadline(model_id, data['deadline'])
    flash('Release model success!')
    return 'success'

@model_creator.route('/model/update', methods=['POST'])
def update_model():
    data = request.get_json()
    update_product(data['id'], data['name'], data['introduction'])
    flash('Update model success!')
    return 'success'

@model_creator.route('/model/delete', methods=['POST'])
def delete_model():
    data = request.get_json()
    model_id = data['id']
    components_id = find_components_id(model_id)
    for component_id in components_id:
        delete_all_propertys(component_id)
    delete_all_components(model_id)
    constraints_id = find_constraints_id(model_id)
    for constraint_id in constraints_id:
        delete_constraint(constraint_id)
    delete_all_constraints(model_id)
    delete_product(model_id)
    flash('Delete model success!')
    return 'success'


