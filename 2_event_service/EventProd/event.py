from flask import Flask, render_template, Response as HTTPResponse, request as HTTPRequest
import mysql.connector, json, pika, logging
from event_producer import *

db = mysql.connector.connect(host="EventSQL", user="root", password="root",database="stellar_event")
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
# /event/ :
# - GET : get all event
# - POST : create new event

# /event/<int:id> :
# - GET : get event by id
# - PUT : update event data
# - DELETE : remove event

@app.route('/event', methods = ['GET', 'POST'])
def event():

    jsondoc = ''

    # # ------------------------------------------------------
    # # * HTTP method = GET (GET ALL ORDERS)
    # # ------------------------------------------------------
    if HTTPRequest.method == 'GET':
        auth = HTTPRequest.authorization
        print(auth)

        # ambil data order
        sql = "SELECT e.*, o.name AS order_name, s.name AS pic_name FROM Event as e INNER JOIN `Order` as o ON e.order_id = o.id INNER JOIN Staff as s ON e.pic_id = s.id"
        dbc.execute(sql)
        events = dbc.fetchall()

        # column_names = [desc[0] for desc in dbc.description]

        if events != None:

            # json_list = []
            for row in events:
                # row_dict = dict(zip(column_names, row))
                # row_dict['schedule'] = row_dict['schedule'].strftime('%Y-%m-%d %H:%M:%S')
                # json_list.append(row_dict)
                row['time_start'] = str(row['time_start'])
                row['time_end'] = str(row['time_end'])

            status_code = 200
            jsondoc = json.dumps(events)

        else: 
            status_code = 404 
            
    # ------------------------------------------------------
    # * HTTP method = POST (NEW ORDER)
    # ------------------------------------------------------
    elif HTTPRequest.method == 'POST':
        data = json.loads(HTTPRequest.data)
        order_id = data['order_id']
        pic_id = data['pic_id']
        name = data['name']
        time_start = data['time_start']
        time_end = data['time_end']

        sql = "INSERT INTO Event (order_id, pic_id, name, time_start, time_end) VALUES (%s, %s, %s, %s, %s);"
        dbc.execute(sql, [order_id, pic_id, name, time_start, time_end])
        db.commit()

        new_event = {
            'event': 'new order',
            'order_id': order_id,
            'pic_id': pic_id,
            'name': name,
            'time_start': time_start,
            'time_end': time_end,
        }

        jsondoc = json.dumps(new_event)
        publish_message(jsondoc,'event.new')
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


@app.route('/event/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
def event2(id):

    jsondoc = ''

    if not str(id).isnumeric():
        status_code = 400  # Bad Request

    # ------------------------------------------------------
    # * HTTP method = GET
    # ------------------------------------------------------
    elif HTTPRequest.method == 'GET':
        auth = HTTPRequest.authorization
        print(auth)

        # ambil data order
        sql = "SELECT e.*, o.name AS order_name, s.name AS pic_name FROM Event as e INNER JOIN `Order` as o ON e.order_id = o.id INNER JOIN Staff as s ON e.pic_id = s.id WHERE e.id=%s"
        dbc.execute(sql, [id])
        event = dbc.fetchone()

        # column_names = [desc[0] for desc in dbc.description]
        # ['id', 'client_id', 'pic_id', 'name', 'category', 'schedule', 'status', 'client_name', 'pic_name']

        if event != None:

            # row_dict = dict(zip(column_names, event))
            # row_dict['schedule'] = row_dict['schedule'].strftime('%Y-%m-%d %H:%M:%S')
            # json_string = json.dumps(row_dict)

            event['time_start'] = str(event['time_start'])
            event['time_end'] = str(event['time_end'])

            status_code = 200
            jsondoc = json.dumps(event)

        else: 
            status_code = 404 

    # ------------------------------------------------------
    # * HTTP method = PUT
    # ------------------------------------------------------
    elif HTTPRequest.method == 'PUT':
        data = json.loads(HTTPRequest.data)
        # order_id = data['order_id']
        pic_id = data['pic_id']
        name = data['name']
        time_start = data['time_start']
        time_end = data['time_end']

        try:
            # ubah nama staff dan gedung di database
            sql = "UPDATE Event SET pic_id=%s, name=%s, time_start=%s, time_end=%s WHERE id=%s;"
            dbc.execute(sql, [pic_id, name, time_start, time_end, id] )
            db.commit()

            updated_event = {
                'event': 'updated event',
                'id': id,
                'pic_id': pic_id,
                'name': name,
                'time_start': time_start,
                'time_end': time_end
            }
            jsondoc = json.dumps(updated_event)
            publish_message(jsondoc,'event.change')

            status_code = 200
            messagelog = 'PUT id: ' + str(id) + ' | name: ' + name + ' | PIC: ' + pic_id + ' | time_start: ' + time_start + ' | time_end: ' + time_end
            logging.warning("Received: %r" % messagelog)

        # bila ada kesalahan saat ubah data, buat XML dengan pesan error
        except mysql.connector.Error as err:
            status_code = 409


    # ------------------------------------------------------
    # * HTTP method = DELETE
    # ------------------------------------------------------
    elif HTTPRequest.method == 'DELETE':
        sql = "SELECT * FROM Event WHERE id = %s;"
        dbc.execute(sql, [id])
        staff = dbc.fetchone()

        if staff is not None:
            sql = "DELETE FROM Event WHERE id = %s;"
            dbc.execute(sql, [id])
            data_delete = {
                "event": "deleted event",
                "id": id
            }

            status_code = 200
            jsondoc = json.dumps(data_delete)
            publish_message(jsondoc,'staff.remove')
        else: 
            status_code = 404
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


@app.route('/order/<int:id>/events', methods = ['GET'])
def event3(id):

    jsondoc = ''

    if not str(id).isnumeric():
        status_code = 400  # Bad Request

    # ------------------------------------------------------
    # * HTTP method = GET
    # ------------------------------------------------------
    elif HTTPRequest.method == 'GET':
        auth = HTTPRequest.authorization
        print(auth)

        # ambil data order
        sql = "SELECT e.*, o.name AS order_name, s.name AS pic_name FROM Event as e INNER JOIN `Order` as o ON e.order_id = o.id INNER JOIN Staff as s ON e.pic_id = s.id WHERE o.id=%s"
        dbc.execute(sql, [id])
        events = dbc.fetchall()

        # column_names = [desc[0] for desc in dbc.description]
        # ['id', 'client_id', 'pic_id', 'name', 'category', 'schedule', 'status', 'client_name', 'pic_name']

        if events != None:

            # json_list = []
            for row in events:
                row['time_start'] = str(row['time_start'])
                row['time_end'] = str(row['time_end'])

            status_code = 200
            jsondoc = json.dumps(events)

        else: 
            status_code = 404 
    
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
