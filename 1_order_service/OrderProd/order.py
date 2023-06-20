from flask import Flask, render_template, Response as HTTPResponse, request as HTTPRequest
import mysql.connector, json, pika, logging
from order_producer import *

db = mysql.connector.connect(host="OrderSQL", user="root", password="root",database="stellar_order")
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
# /order/ :
# - GET : get all order
# - POST : create new order

# /order/<int:id> :
# - GET : get order by id
# - PUT : update order data
# - DELETE : remove order

@app.route('/order', methods = ['GET', 'POST'])
def order():
    jsondoc = ''

    # if HTTPRequest.method not in app._method_route:
    #     status_code = 400  # Bad Request

    # # ------------------------------------------------------
    # # * HTTP method = GET (GET ALL ORDERS)
    # # ------------------------------------------------------
    # el
    if HTTPRequest.method == 'GET':
        auth = HTTPRequest.authorization
        print(auth)

        # ambil data staff
        sql = "SELECT * FROM `Order`"
        dbc.execute(sql)
        orders = dbc.fetchall()

        if orders != None:
            # Convert datetime objects to strings
            orders = [order for order in orders]
            for order in orders:
                order['schedule'] = order['schedule'].strftime('%Y-%m-%d %H:%M:%S')

            status_code = 200
            jsondoc = json.dumps(orders)
        else: 
            status_code = 404 
            
    # ------------------------------------------------------
    # * HTTP method = POST (NEW ORDER)
    # ------------------------------------------------------
    elif HTTPRequest.method == 'POST':
        data = json.loads(HTTPRequest.data)
        client_id = data['client_id']
        pic_id = data['pic_id']
        name = data['name']
        category = data['category']
        schedule = data['schedule']
        status = 'Scheduled'

        sql = "INSERT INTO `Order` (client_id, pic_id, name, category, schedule, status) VALUES (%s, %s, %s, %s, %s, %s)"
        dbc.execute(sql, [client_id, pic_id, name, category, schedule, status])
        db.commit()

        new_order = {
            'client_id': client_id,
            'pic_id': pic_id,
            'name': name,
            'category': category,
            'schedule': schedule,
            'status': status
        }

        jsondoc = json.dumps(new_order)
        publish_message(jsondoc,'order.new')
        status_code = 201
    else:
        status_code = 400

    # ------------------------------------------------------
    # Kirimkan JSON yang sudah dibuat ke staff
    # ------------------------------------------------------
    resp = HTTPResponse()
    if jsondoc !='': resp.response = jsondoc
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp


@app.route('/order/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
def order2(id):

    jsondoc = ''

    if not id.isnumeric() or HTTPRequest.method not in app._method_route:
        status_code = 400  # Bad Request

    # ------------------------------------------------------
    # * HTTP method = GET
    # ------------------------------------------------------
    elif HTTPRequest.method == 'GET':
            
        sql = "SELECT * FROM `Order` WHERE id = %s"
        dbc.execute(sql, [id])
        order = dbc.fetchone()
        
        if order != None:
            status_code = 200
            jsondoc = json.dumps(order)
        else: 
            status_code = 404 

    # ------------------------------------------------------
    # * HTTP method = PUT
    # ------------------------------------------------------
    elif HTTPRequest.method == 'PUT':
        data = json.loads(HTTPRequest.data)
        # client_id = data['client_id'] # gak butuh
        pic_id = data['pic_id']
        name = data['name']
        # category = data['category'] # gak butuh
        schedule = data['schedule']
        status = data['status']

        try:
            # ubah nama staff dan gedung di database
            sql = "UPDATE Staff SET pic_id=%s, name=%s, schedule=%s, status=%s WHERE id=%s"
            dbc.execute(sql, [pic_id, name, schedule, status, id] )
            db.commit()

            updated_order = {
                'event': 'updated_order',
                'id': id,
                'name': name,
                'schedule': schedule,
                'status': status
            }
            jsondoc = json.dumps(updated_order)
            publish_message(jsondoc,'order.change')

            status_code = 200
            messagelog = 'PUT id: ' + str(id) + ' | name: ' + name + ' | schedule: ' + schedule + ' | status: ' + status
            logging.warning("Received: %r" % messagelog)

        # bila ada kesalahan saat ubah data, buat XML dengan pesan error
        except mysql.connector.Error as err:
            status_code = 409


    # ------------------------------------------------------
    # * HTTP method = DELETE
    # ------------------------------------------------------
    elif HTTPRequest.method == 'DELETE':
        sql = "SELECT * FROM Order WHERE id = %s"
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

    # ------------------------------------------------------
    # Kirimkan JSON yang sudah dibuat ke staff
    # ------------------------------------------------------
    resp = HTTPResponse()
    if jsondoc !='': resp.response = jsondoc
    resp.headers['Content-Type'] = 'application/json'
    resp.status = status_code
    return resp





