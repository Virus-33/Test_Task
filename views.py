from modules import back
from modules import DB_Access
from flask import Flask, redirect, session
from flask import render_template, request
from flask_login import LoginManager, login_user, logout_user, current_user

app = Flask(import_name='TestApp')
app.debug = True
app.secret_key = 'something secret'

lm = LoginManager()
lm.init_app(app)


@lm.user_loader
def loader_user(user_id):
    return DB_Access.get_by_id(user_id)


@app.route('/submit/reg', methods=['POST'])
def user_register():
    login = request.form['Login']
    password = request.form['Password']
    passcon = request.form['ConfirmPassword']
    if not set("()'\",").isdisjoint(login):
        return render_template('err_reg.html', er_type='login')
    if password != passcon:
        return render_template('err_reg.html', er_type='pass')
    back.register(login, password)
    return render_template('login.html')


@app.route('/submit/log', methods=['POST'])
def user_logon():
    login = request.form['Login']
    password = request.form['Password']
    if not set("()'\",").isdisjoint(login):
        return render_template('err_login.html')
    user = back.check_user(login, password)
    if user is None:
        return render_template('err_login.html')
    login_user(user)
    users = DB_Access.get_users()
    session['user_id'] = user.id
    return display_user(user, users)


@app.route('/')
@app.route('/login')
def logging_page() -> str:
    """Displays login page.
    Returns:
        Template as str"""
    return render_template('login.html')


@app.route('/register', methods=['GET'])
def register_page():
    """Displays register page.
    Returns:
        Template as str"""
    return render_template('register.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@app.route('/deletion')
def delete():
    u_id = session['user_id']
    logout_user()
    DB_Access.delete_user(u_id)
    return redirect('/login')


def display_user(user, users):
    return render_template('user_page.html', title=user.login, current_user=user, list=users)


app.run()
