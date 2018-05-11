import sys
sys.path.append("..")

from flask import Flask, render_template, request
from Configuration.controller.order_generator import order_generator
from Configuration.controller.home import home

app = Flask(__name__)
app.register_blueprint(order_generator)
app.register_blueprint(home)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
@app.route('/')
def index():
    phone_num = request.cookies.get('user_email')
    if phone_num is not None:
        print('=====> ', phone_num, 'logged in')
        return render_template('home.html', login=False)
    else:
        return render_template('home.html', login=False)
