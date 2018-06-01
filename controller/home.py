# -*- coding: utf-8 -*-
from flask import Blueprint,flash, redirect, url_for, render_template, request, make_response, session
from Configuration.inventory.user_inv import insert_user, find_user_by_email
from Configuration.model.user import User
import smtplib
from email.mime.text import MIMEText

home = Blueprint('home', __name__, template_folder='templates')


@home.route('/login', methods=['POST'])
def login():
    log_email = request.form.get('log_email')
    password = request.form.get('log_pswd')
    user = find_user_by_email(log_email)
    print('========>', log_email)
    print('========>', password)
    print('========>', user.password)
    if user.password == password:
        resp = make_response(render_template('home.html', login=True, user=user))
        resp.set_cookie('user_email', log_email)
        session['user_email'] = log_email
        session['user_role'] =user.role
        return resp
    else:
        return render_template('home.html', login=False, user=user)


# Send the message via our own SMTP server.
server = smtplib.SMTP_SSL()

@home.route('/register', methods=['POST'])
def register():
    reg_email = request.form.get('log_email')
    name = request.form.get('log_name')
    password = request.form.get('log_pswd')
    user = User(reg_email, name, password, 1, '', '')
    server.connect('smtp.qq.com', 465)
    server.login("193559882", "idhqibmcwajmbjgb")
    mail_text = '''<body>欢迎您注册Config，请单击如下链接验证邮箱，以完成注册，谢谢！
    <br><a href='http://localhost:5000/validate?name=%s'>注册验证</a></body>'''\
    % name
    msg = MIMEText(mail_text, 'html')
    msg['Subject'] = 'CONFIG 邮箱验证'
    from_addr = '193559882@qq.com'
    msg['From'] = from_addr
    msg['To'] = reg_email
    server.sendmail(from_addr, reg_email, msg.as_string())
    server.quit()
    session[name] = user.toJSON()
    return '一封验证邮件已经发送到您的邮箱，请查看并进行验证，谢谢！'

@home.route('/validate')
def validate():
    user_name =  request.args.get('name', '')
    import json
    user = lambda: None
    user.__dict__ = json.loads(session[user_name])
    try:
        insert_user(user)
        session.pop(user_name, None)
        flash('register success!')
        return redirect(url_for('index'))
    except Exception as e:
        session.pop(user_name, None)
        return 'register failure'
