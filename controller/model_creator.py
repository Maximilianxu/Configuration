# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, session

model_creator = Blueprint('model_creator', __name__, template_folder='templates')

@model_creator.route('/model')
def model():
    return render_template('model.html')

