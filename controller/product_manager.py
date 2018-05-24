from flask import Blueprint, render_template, request, session
from Configuration.inventory.product_inv import find_products_id_name_for_expert, find_products_id_name_for_customer,\
    update_realease


product_manager = Blueprint('product_manager', __name__, template_folder='templates')

@product_manager.route('/products')
def product():
    user_email = session['user_email']
    user_role = session['user_role']
    if(user_role == 0):
        products = find_products_id_name_for_expert(user_email)
    else:
        products = find_products_id_name_for_customer()
    return render_template('product.html', user_role=user_role, products=products)

@product_manager.route('/product/stop_release', methods=['POST'])
def stop_release_product():
    data = request.get_json()
    product_id = data['id']
    update_realease(0, product_id)
    return 'success'