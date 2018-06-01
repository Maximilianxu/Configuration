import sys
sys.path.append("..")

from flask import Flask, render_template, request
from Configuration.controller.order_generator import order_generator
from Configuration.controller.home import home
from Configuration.controller.product_manager import product_manager
from Configuration.controller.model_manager import model_manager
from Configuration.controller.component_manager import component_manager
from Configuration.controller.property_manager import property_manager
from Configuration.controller.constraint_manager import constraint_manager
from Configuration.inventory.user_inv import find_user_by_email


app = Flask(__name__)
app.register_blueprint(order_generator)
app.register_blueprint(home)
app.register_blueprint(product_manager)
app.register_blueprint(model_manager)
app.register_blueprint(component_manager)
app.register_blueprint(property_manager)
app.register_blueprint(constraint_manager)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/')
def index():
    email = request.cookies.get('user_email')
    user = find_user_by_email(email)
    if email is not None:
        print('=====> ', email, 'logged in')        
        return render_template('home.html', login=True, user=user)
    else:
        return render_template('home.html', login=False, user=user)

app.run(debug=True)
