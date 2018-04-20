from flask import Flask
from Configuration.controller.order_generator import order_generator

app = Flask(__name__)
app.register_blueprint(order_generator)