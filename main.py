import sys
sys.path.append("..")

from flask import Flask, render_template, request
from Configuration.controller.order_generator import order_generator
from Configuration.controller.home import home
from Configuration.controller.model_creator import model_creator
from Configuration.controller.component_creator import component_creator
from Configuration.controller.property_manager import property_manager

app = Flask(__name__)
app.register_blueprint(order_generator)
app.register_blueprint(home)
app.register_blueprint(model_creator)
app.register_blueprint(component_creator)
app.register_blueprint(property_manager)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/')
def index():
    phone_num = request.cookies.get('user_email')
    if phone_num is not None:
        print('=====> ', phone_num, 'logged in')
        return render_template('home.html', login=True)
    else:
        return render_template('home.html', login=False)

app.run(debug=True)
