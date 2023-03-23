#Methoden um den User einzuloggen und den User zu registrieren
#Eigenentwicklung

from flask import render_template, request, session, redirect, url_for
from app.app import app
from helpers.db import execute_query
from helpers.password import verify_password


@app.route("/do-login", methods=('POST',))
def do_login():
    email = request.form.get('email')
    password = request.form.get('password')
#Prüfen ob User existiert
    rows = execute_query('SELECT * FROM user WHERE email = %s', [email])
    if len(rows) == 0:
        session['wrong_credentials_msg'] = 'Email or Password is wrong.'
        return redirect(url_for('login'))
#Prüfen ob Passwort stimmt
    row = rows[0]
    if not verify_password(password, row['password']):
        session['wrong_credentials_msg'] = 'Email or Password is wrong.'
        return redirect(url_for('login'))
#Prüfen ob Status aktiv
    if row['status'] != 'active':
        session['wrong_credentials_msg'] = 'Please contact admin to update your status.'
        return redirect(url_for('login'))

    session['user_id'] = row['id']
    return redirect(url_for('home'))


#Rendering der Loginform und prüfen der eingegebenen Informationen
@app.route("/login")
def login():
    user_id = session.get('user_id')
    if user_id is not None:
        return redirect(url_for('home'))

    wrong_credentials_msg = session.get('wrong_credentials_msg')
    if wrong_credentials_msg is not None:
        session.pop('wrong_credentials_msg')
    else:
        wrong_credentials_msg = ''

    return render_template('login/login.html', wrong_credentials_msg=wrong_credentials_msg)
