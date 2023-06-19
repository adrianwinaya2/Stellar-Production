from flask import Flask, render_template, Response as HTTPResponse, request as HTTPRequest
import mysql.connector, json, pika, logging
from staff_producer import *

db = mysql.connector.connect(host="StaffSQL", user="root", password="root",database="stellar_staff")
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
# /staff/ :
#   - GET : get all staff

# /staff/<id:int> :
#   - GET : get 1 staff by id
#   - PUT : update staff data
#   - DELETE : remove staff

# /staff/<positioin:str> :
#   - GET : get all staff with desired position


@app.route('/staff', methods = ['GET'])
def staff():
    jsondoc = ''

    if HTTPRequest.method not in app._method_route:
        status_code = 400  # Bad Request

    # ------------------------------------------------------
    # * HTTP method = GET
    # ------------------------------------------------------
    elif HTTPRequest.method == 'GET':
        auth = HTTPRequest.authorization
        print(auth)

        # ambil data staff
        sql = "SELECT * FROM Staff"
        dbc.execute(sql)
        staffs = dbc.fetchall()

        if staffs != None:
            status_code = 200
            jsondoc = json.dumps(staffs)
        else: 
            status_code = 404 

    # ------------------------------------------------------
    # Kirimkan JSON yang sudah dibuat ke staff
    # ------------------------------------------------------
    resp = HTTPResponse()
    if jsondoc !='': resp.response = jsondoc
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp


@app.route('/staff/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
def staff2(id):

    jsondoc = ''

    if not id.isnumeric() or HTTPRequest.method not in app._method_route:
        status_code = 400  # Bad Request

    # ------------------------------------------------------
    # * HTTP method = GET
    # ------------------------------------------------------
    elif HTTPRequest.method == 'GET':
            
        sql = "SELECT * FROM Staff WHERE id = %s"
        dbc.execute(sql, [id])
        staff = dbc.fetchone()
        
        if staff != None:
            status_code = 200
            jsondoc = json.dumps(staff)
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
        position = data['position']

        try:
            # ubah nama staff dan gedung di database
            sql = "UPDATE Staff SET username=%s, name=%s, email=%s, position=%s, WHERE id=%s"
            dbc.execute(sql, [username, name, email, position] )
            db.commit()

            # teruskan json yang berisi perubahan data staff yang diterima dari Web UI
            # ke RabbitMQ disertai dengan tambahan route = 'staff.tenant.changed'
            data_update = {
                'event': 'updated_staff',
                'id': id,
                'username': username,
                'name': name,
                'email': email,
                'position': position,
            }
            jsondoc = json.dumps(data_update)
            publish_message(jsondoc,'staff.change')

            status_code = 200
            messagelog = 'PUT id: ' + str(id) + ' | username: ' + username + ' | name: ' + name + ' | email: ' + email + ' | position: ' + position
            logging.warning("Received: %r" % messagelog)

        # bila ada kesalahan saat ubah data, buat XML dengan pesan error
        except mysql.connector.Error as err:
            status_code = 409


    # ------------------------------------------------------
    # * HTTP method = DELETE
    # ------------------------------------------------------
    elif HTTPRequest.method == 'DELETE':
        sql = "SELECT * FROM Staff WHERE id = %s"
        dbc.execute(sql, [id])
        staff = dbc.fetchone()

        if staff is not None:
            sql = "DELETE FROM Staff WHERE id = %s"
            dbc.execute(sql, [id])
            data_delete = {"id": id}

            status_code = 200
            jsondoc = json.dumps(data_delete)
            publish_message(jsondoc,'staff.remove')
        else: 
            status_code = 404
    
    else:
        status_code = 400  # Bad Request


    # ------------------------------------------------------
    # Kirimkan JSON yang sudah dibuat ke staff
    # ------------------------------------------------------
    resp = HTTPResponse()
    if jsondoc !='': resp.response = jsondoc
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp

@app.route('/staff/<string:position>', methods = ['GET'])
def staff3(position):

    jsondoc = ''

    if type(position) != str or position not in ['leader', 'coordinator', 'member']:
        status_code = 400  # Bad Request

    elif HTTPRequest.method == 'GET':
        auth = HTTPRequest.authorization
        print(auth)

        # ambil data staff
        sql = "SELECT * FROM Staff WHERE position = %s"
        dbc.execute(sql, [position])
        staffs = dbc.fetchall()

        if staffs != None:
            status_code = 200
            jsondoc = json.dumps(staffs)
        else: 
            status_code = 404

    # ------------------------------------------------------
    # Kirimkan JSON yang sudah dibuat ke staff
    # ------------------------------------------------------
    resp = HTTPResponse()
    if jsondoc !='': resp.response = jsondoc
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp
