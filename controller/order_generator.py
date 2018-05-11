# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request
order_generator = Blueprint('order_generator', __name__, template_folder='templates')

@order_generator.route('/config')
def order():
    return render_template('config.html')

@order_generator.route('/order/reqs', methods=['POST'])
def sub_reqs():
    reqs = request.get_json()
    from Configuration.main import app
    for req in reqs:
        app.logger.debug(str(req))
        app.logger.debug(type(str(req)))
    # 可以join之后作为一个string，作为求解器的reqs
    return 'success'

@order_generator.route('/order/new', methods=['POST'])
def sub_order():
    # 变量赋值情况以及总价格
    data = request.get_json()
    from Configuration.main import app
    assignments = data['assignments']
    price = data['price']
    app.logger.debug(assignments)
    app.logger.debug(price)
    return 'success'