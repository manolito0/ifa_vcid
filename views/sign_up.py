
#Methoden um neuen User hinzuzufügen und Datenprüfung
#Eigenentwicklung

from flask import render_template, request, session, redirect, url_for
from app.app import app
from helpers.db import execute_query, insert
from helpers.password import generate_password


# DB Eintrag erstellen
@app.route("/do_sign_up", methods=('POST',))
def do_sign_up():
    email = request.form.get('email')
    user_name = request.form.get('user_name')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    # Überprüfen ob Passwort stimmt
    if not (password == confirm_password):
        session['wrong_credentials_msg'] = 'Confirm Password mismatch.'
        return redirect(url_for('sign_up'))

    # Doppelte Email Adresse prüfen
    rows = execute_query('SELECT * FROM user WHERE email = %s', [email])
    if len(rows) > 0:
        session['wrong_credentials_msg'] = 'Given email already exists.'
        return redirect(url_for('sign_up'))

    # User in DB adden
    status, result = insert("""
        INSERT INTO user (email, password, user_name, status)
        VALUES
        (%s, %s, %s, 'active')
    """, [email, generate_password(password), user_name])
    # Fehler handling
    if status:
        session['user_id'] = result.lastrowid
        return redirect(url_for('home'))
    else:
        session['wrong_credentials_msg'] = 'An error occured'
        print(result)
        return redirect(url_for('sign_up'))


# Rendering des Registrierungsformulars 
@app.route("/sign_up")
def sign_up():
    user_id = session.get('user_id')
    if user_id is not None:
        return redirect(url_for('home'))

    wrong_credentials_msg = session.get('wrong_credentials_msg')
    if wrong_credentials_msg is not None:
        session.pop('wrong_credentials_msg')
    else:
        wrong_credentials_msg = ''

    return render_template('login/sign-up.html', wrong_credentials_msg=wrong_credentials_msg)
