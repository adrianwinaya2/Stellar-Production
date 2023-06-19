from flask import Flask, render_template, Response as HTTPResponse, request as HTTPRequest
import mysql.connector, json, pika, logging
from client_producer import *

db = mysql.connector.connect(host="ClientSQL", user="root", password="root",database="stellar_client")
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
# /client/ :
#   - GET : get all client

# /client/<id> :
#   - GET : get 1 client by id
#   - PUT : update client data
#   - DELETE : remove client


@app.route('/client', methods = ['GET'])
def client():
    jsondoc = ''


    # ------------------------------------------------------
    # * HTTP method = GET
    # ------------------------------------------------------
    if HTTPRequest.method == 'GET':
        auth = HTTPRequest.authorization
        print(auth)

        # ambil data client
        sql = "SELECT * FROM Client"
        dbc.execute(sql)
        clients = dbc.fetchall()

        if clients != None:
            status_code = 200
            jsondoc = json.dumps(clients)
        else: 
            status_code = 404 

    # ------------------------------------------------------
    # Kirimkan JSON yang sudah dibuat ke client
    # ------------------------------------------------------
    resp = HTTPResponse()
    if jsondoc !='': resp.response = jsondoc
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp


@app.route('/client/<path:id>', methods = ['GET', 'PUT', 'DELETE'])
def client2(id):

    if not id.isnumeric():
        status_code = 400  # Bad Request
    
    jsondoc = ''

    # ------------------------------------------------------
    # * HTTP method = GET
    # ------------------------------------------------------
    if HTTPRequest.method == 'GET':
            
        sql = "SELECT * FROM Client WHERE id = %s"
        dbc.execute(sql, [id])
        client = dbc.fetchone()
        
        if client != None:
            status_code = 200
            jsondoc = json.dumps(client)
        else: 
            status_code = 404 

    # ------------------------------------------------------
    # * HTTP method = PUT
    # ------------------------------------------------------
    elif HTTPRequest.method == 'PUT':
        data = json.loads(HTTPRequest.data)
        username = data['username']
        name = data['name']
        email = data['email']

        try:
            # ubah data client di database
            sql = "UPDATE Client SET username=%s, name=%s, email=%s, WHERE id=%s"
            dbc.execute(sql, [username, name, email, id] )
            db.commit()

            # teruskan json yang berisi perubahan data client yang diterima dari Web UI
            # ke RabbitMQ disertai dengan tambahan route = 'client.tenant.changed'
            data_update = {
                'event': 'updated_client',
                'id': id,
                'username': username,
                'name': name,
                'email': email,
            }
            jsondoc = json.dumps(data_update)
            publish_message(jsondoc,'client.change')

            status_code = 200
            messagelog = 'PUT id: ' + str(id) + ' | username: ' + username + ' | name: ' + name + ' | email: ' + email
            logging.warning("Received: %r" % messagelog)

        # bila ada kesalahan saat ubah data, buat XML dengan pesan error
        except mysql.connector.Error as err:
            status_code = 409


    # ------------------------------------------------------
    # * HTTP method = DELETE
    # ------------------------------------------------------
    elif HTTPRequest.method == 'DELETE':
        sql = "SELECT * FROM Client WHERE id = %s"
        dbc.execute(sql, [id])
        client = dbc.fetchone()

        if client is not None:
            sql = "DELETE FROM Client WHERE id = %s"
            dbc.execute(sql, [id])
            data_delete = {"id": id}

            status_code = 200
            jsondoc = json.dumps(data_delete)
            publish_message(jsondoc,'client.remove')
        else: 
            status_code = 404

    # ------------------------------------------------------
    # Kirimkan JSON yang sudah dibuat ke client
    # ------------------------------------------------------
    resp = HTTPResponse()
    if jsondoc !='': resp.response = jsondoc
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp





