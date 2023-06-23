from flask import Flask, render_template, Response as HTTPResponse, request as HTTPRequest, session
import mysql.connector, json, pika, logging
from account_producer import *

db = mysql.connector.connect(host="AccountSQL", user="root", password="root",database="stellar_account")
dbc = db.cursor(dictionary=True)


app = Flask(__name__)

# Note, HTTP response codes are
#  200 = OK the request has succeeded.
#  201 = the request has succeeded and a new resource has been created as a result.    
#  401 = Unauthorized (user identity is unknown)
#  403 = Forbidden (user identity is known to the server)
#  409 = A conflict with the current state of the resource
#  429 = Too Many Requests

# ! DOCUMENTATION
# /create_account/<string:role> :
# - POST : register account

# /authenticate/<string:role> :
#  - POST : login account


@app.route('/register/', methods = ['POST'])
def register():
    
    jsondoc = ''

    # ------------------------------------------------------
    # HTTP method = POST
    # ------------------------------------------------------
    if HTTPRequest.method == 'POST':
        data = json.loads(HTTPRequest.data)
        # event = data['event']
        name = data['name']
        username = data['username']
        password = data['password']
        role = data['role']
        email = data['email']
        position = data['position']

        # check username availability
        sql = "SELECT id FROM Account WHERE username=%s;"
        dbc.execute(sql, [username])
        account = dbc.fetchone()

        if account:
            status_code = 409
            jsondoc = json.dumps({'status': 'failed', 'message': 'Username already exist'})
        else:
            try:
                # simpan nama kantin, dan gedung ke database
                sql = "INSERT INTO Account (username, password, role) VALUES (%s, %s, %s);"
                dbc.execute(sql, [username, password, role] )
                db.commit()

                # dapatkan ID dari data kantin yang baru dimasukkan
                new_data = {
                    'event': 'new account',
                    'username': username,
                    'role': role,
                    'name': name,
                    'email': email,
                    'position': position
                }
                jsondoc = json.dumps(new_data)
                route_key = 'staff.new' if role == 'Staff' else 'client.new'
                publish_message(jsondoc, route_key)

                status_code = 201
                session['client_id'] = account[0]
                
            except mysql.connector.Error as err:
                status_code = 409

    else:
        status_code = 400  # Bad Request


    # ------------------------------------------------------
    # Kirimkan JSON yang sudah dibuat ke client
    # ------------------------------------------------------
    resp = HTTPResponse()
    if jsondoc !='': resp.response = jsondoc
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp


@app.route('/authenticate', methods = ['POST'])
def authenticate():
    jsondoc = ''

    # ------------------------------------------------------
    # HTTP method = POST
    # ------------------------------------------------------
    if HTTPRequest.method == 'POST':
        data = json.loads(HTTPRequest.data)
        # event = data['event']
        # role = data['role']
        username = data['username']
        password = data['password']

        try:
            # simpan nama kantin, dan gedung ke database
            sql = "SELECT id, password FROM Account WHERE username=%s;"
            dbc.execute(sql, [username] )
            account = dbc.fetchone()

            if account and account[0] == password:
                status_code = 200
                session['client_id'] = account[0]
                jsondoc = json.dumps({'status': 'success'})
            else:
                status_code = 401
                jsondoc = json.dumps({'status': 'failed'})
                
            
        except mysql.connector.Error as err:
            status_code = 409
    
    else:
        status_code = 400 # Bad Request

    # ------------------------------------------------------
    # Kirimkan JSON yang sudah dibuat ke client
    # ------------------------------------------------------
    resp = HTTPResponse()
    if jsondoc !='': resp.response = jsondoc
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp