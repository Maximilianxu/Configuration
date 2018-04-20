from flask import Blueprint, render_template
order_generator = Blueprint('order_generator', __name__, template_folder='templates')

@order_generator.route('/order')
def order():
    return render_template('order.html')