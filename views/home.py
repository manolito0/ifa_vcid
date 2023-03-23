
#Methoden um alle Termine Anzuzeigen und den User auszuloggen
#Eigenentwicklung

from flask import render_template, session, redirect, url_for
from app.app import app
from helpers.db import execute_query

# Methode für die Terminübersicht
@app.route("/")
def home():
#Überprüfung ob der User eingeloggt ist, ansonsten Login Prompt
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login'))
#Anzeige der einzelnen Termine
    rows = execute_query('SELECT * FROM user WHERE id = %d' % user_id)
    if len(rows) == 0:
        session.pop('user_id')
        return redirect(url_for('login'))
#Check ob User aktiv
    user_data = rows[0]
    if user_data['status'] != 'active':
        session.pop('user_id')
        session['wrong_credentials_msg'] = 'Please contact admin to update your status.'
        return redirect(url_for('login'))

    jobs = execute_query('SELECT j.*, u.user_name FROM jobs j INNER JOIN user u on u.id = j.created_by')
    return render_template('home/home.html', user_data=user_data, jobs=jobs)

#Methode für Logout
@app.route("/logout")
def logout():
    session.pop('user_id')
    return redirect(url_for('login'))
