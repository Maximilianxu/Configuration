# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, session, jsonify
import datetime
from Configuration.inventory.component_inv import find_subcomponents_id_name
from Configuration.inventory.order_inv import find_all_orders_by_email, insert_order
from Configuration.model.order import Order
from Configuration.model.task import Task
order_generator = Blueprint('order_generator', __name__, template_folder='templates')
import redis

@order_generator.route('/config')
def config():
    root_component_id = session['root_component_id']
    root_component_name = session['root_component_name']
    subcomponents = find_subcomponents_id_name(root_component_id)
    r = redis.Redis(host='localhost', port=6379)
    prod_id = session['model_id']
    task = Task()
    r.set(prod_id, task)
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
    reqs = request.get_json()
    print(reqs)

    return 'success'

@order_generator.route('/order/new', methods=['POST'])
def sub_order():
    # 变量赋值情况以及总价格
    data = request.get_json()
    from Configuration.main import app
    assignments = data['assignments']
    price = data['price']
    user_email = session['user_email']
    ord = Order(user_email, 0, assignments, datetime.date.today(), price, 'up')
    insert_order(ord)
    return 'success'