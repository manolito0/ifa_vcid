'''
Methode um alle Termine via API Call abzurufen
'''

# Import der Module 
import json
from flask import Response

from app.app import app
from helpers.db import execute_query

# Date Time Json Encoder
class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)


# API Route definieren
@app.route("/api/list")
def api_list():
    rows = execute_query('SELECT j.*, u.user_name FROM jobs j INNER JOIN user u on u.id = j.created_by')
    return Response(json.dumps(rows, cls=DatetimeEncoder), mimetype='application/json')
