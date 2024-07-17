from modules import back
from modules import DB_Access
from flask import Flask, redirect, session
from flask import render_template, request
from flask_login import LoginManager, login_user, logout_user

# Creating Flask application
app = Flask(import_name='TestApp')
app.debug = True
app.secret_key = 'something secret'

# Creating login manager
lm = LoginManager()
lm.init_app(app)


@lm.user_loader
def loader_user(user_id):
    """
    Provides user object from id stored in session
    :param user_id:
    :return: user object
    """
    return DB_Access.get_by_id(user_id)


@app.route('/submit/reg', methods=['POST'])  # Defined method to prevent page opened with GET
def user_register():
    """
    Checks passwords and special symbols to prevent SQLi.
    :return: Rendered template as str
    """
    login = request.form['Login']
    password = request.form['Password']
    passcon = request.form['ConfirmPassword']
    if not set("()'\",").isdisjoint(login):  # spec symbols checking
        return render_template('err_reg.html', er_type='login')
    if password != passcon:
        return render_template('err_reg.html', er_type='pass')
    back.register(login, password)  # Call to create user in database
    return render_template('login.html')


@app.route('/submit/log', methods=['POST'])  # Defined method to prevent page opened with GET
def user_logon():
    """
    Checks login for spec symbols, tries to let user in. Changes layout on success.
    :return:
    """
    login = request.form['Login']
    password = request.form['Password']
    if not set("()'\",").isdisjoint(login):  # spec symbols checking
        return render_template('err_login.html')
    user = back.check_user(login, password)  # Call to check user's existance
    if user is None:
        return render_template('err_login.html')  # Render error if user not found
    login_user(user)  # log user in via login manager on success
    users = DB_Access.get_users()  # Call to get all users nicknames
    session['user_id'] = user.id  # Store user's id in session
    return display_user(user, users)  # Call for render user page


@app.route('/')
@app.route('/login')
def logging_page() -> str:
    """
    Displays login page
    :return: Rendered template as str
    """
    return render_template('login.html')


@app.route('/register', methods=['GET'])
def register_page():
    """
    Displays register page
    :return: Rendered template as str
    """
    return render_template('register.html')


@app.route('/logout')
def logout():
    """
    Logout user
    :return: Rendered template as str
    """
    logout_user()
    return redirect('/login')


@app.route('/deletion')
def delete():
    """
    Deletes user from database
    :return: Rendered template as str
    """
    u_id = session['user_id']  # Get user's id from session info
    logout_user()
    DB_Access.delete_user(u_id)  # Call to delete user from database
    return redirect('/login')  # Redirect user to login page


def display_user(user, users):
    """
    Renders user page without redirecting. Maybe I should've done al such stuff this way.
    :param user: currently active user as user object
    :param users: list of users nicknames
    :return: Rendered template with substituted values as str
    """
    return render_template('user_page.html', title=user.login, current_user=user, list=users)


# Start Flask app
app.run()
