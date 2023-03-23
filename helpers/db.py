#Setup der MySQL Datenbank

from flask_mysqldb import MySQL
from app.app import app

# MySQL Datenbank Connection String
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'vcid_user01'
app.config['MYSQL_PASSWORD'] = 'Pa$$word069'
app.config['MYSQL_DB'] = 'dogsitting'

app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

#Funktion um Daten zu lesen
def execute_query(query, params=[]):
    cursor = mysql.connection.cursor()
    cursor.execute(query, params)
    return cursor.fetchall()

#Funktion um Daten zu schreiben
def insert(query, params=[], commit=True):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(query, params)

        if commit:
            mysql.connection.commit()

        return True, cursor
    except Exception as e:
        return False, str(e)
