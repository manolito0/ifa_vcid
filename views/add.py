
#Methoden für das Hinzufügen eines und bearbeiten eines Termins
#Eigenentwicklung

from flask import render_template, request, session, redirect, url_for
from app.app import app
from helpers.db import insert, execute_query


# Definieren der Variablen der einzelnen Formularfelder
@app.route("/do_add", methods=('POST',))
def do_add():
    dog_name = request.form.get('dog_name')
    owner_name = request.form.get('owner_name')
    owner_address = request.form.get('owner_address')
    date_from = request.form.get('date_from')
    date_to = request.form.get('date_to')
    time_from = request.form.get('time_from')
    time_to = request.form.get('time_to')
    status = request.form.get('status')

    user_id = session.get('user_id')

    #Hinzufügen des Termins in in die Datenbank
    status, result = insert("""
        INSERT INTO jobs (dog_name, owner_name, owner_address, date_from, date_to, time_from, time_to, status, created_by)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, [dog_name, owner_name, owner_address, date_from, date_to, time_from, time_to, status, user_id])

    if status:
        session['success_msg'] = 'Erfolgreich'
        return redirect(url_for('home'))
    else:
        session['error_msg'] = 'Fehler'
        print(result)
        return redirect(url_for('add'))


# Methode um das Formular zu rendern und die entsprechenden Werte in die DB zu schreiben
@app.route("/add")
def add():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login'))

    return render_template('list/add.html', id=0, action='/do_add', data={
        'dog_name': '',
        'owner_name': '',
        'owner_address': '',
        'date_from': '',
        'date_to': '',
        'time_from': '',
        'time_to': '',
        'status': 'New',
    })


# Methode um einen erfassten Termin zu löschen 
@app.route("/delete/<job_id>")
def delete(job_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login'))

    status, result = insert('DELETE FROM jobs WHERE job_id = %s', [job_id])
    return redirect(url_for('home'))


# Methode um ein bereits erfassten Termin zu aktualisieren
@app.route("/do_edit", methods=('POST',))
def do_edit():
    dog_name = request.form.get('dog_name')
    owner_name = request.form.get('owner_name')
    owner_address = request.form.get('owner_address')
    date_from = request.form.get('date_from')
    date_to = request.form.get('date_to')
    time_from = request.form.get('time_from')
    time_to = request.form.get('time_to')
    status = request.form.get('status')

    id = request.form.get('id')

    # DB Query für Updates
    status, result = insert("""
        UPDATE jobs SET dog_name = %s, owner_name = %s, owner_address = %s, date_from = %s, date_to = %s, time_from = %s, time_to = %s, status = %s
        WHERE job_id = %s
        """, [dog_name, owner_name, owner_address, date_from, date_to, time_from, time_to, status, id])

    @Error handling
    if status:
        session['success_msg'] = 'Erfolgreich'
        return redirect(url_for('home'))
    else:
        session['error_msg'] = 'Fehler'
        print(result)
        return redirect(url_for('home'))


@app.route("/edit/<job_id>")
def edit(job_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login'))

    rows = execute_query('SELECT * FROM jobs WHERE job_id = %s', [job_id])
    if len(rows) == 0:
        return redirect(url_for('home'))

    return render_template('list/add.html', id=job_id, action='/do_edit', data=rows[0])
