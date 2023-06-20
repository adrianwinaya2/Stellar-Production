import pika, sys, os
import mysql.connector,logging, json


db = mysql.connector.connect(host="EventSQL", user="root", password="root",database="stellar_event")
dbc = db.cursor(dictionary=True)


def main():
    def check_db_order(id):
        sql = "SELECT * FROM Order WHERE id = %s"
        dbc.execute(sql, [id])
        order = dbc.fetchone()
        return True if order else False
    
    def check_db_staff(id):
        sql = "SELECT * FROM Staff WHERE id = %s"
        dbc.execute(sql, [id])
        staff = dbc.fetchone()
        return True if staff else False
    
    def get_message(ch, method, properties, body):

        # Parse json data di dalam 'body' untuk mengambil data terkait event
        route = method.routing_key
        data = json.loads(body)
        event = data['event']

        if route == "order.new":
            name = data['name']
            schedule = data['schedule']

            sql = "INSERT INTO `Order` (name, schedule) VALUES (%s, %s);"
            dbc.execute(sql, [name, schedule])
        
        elif route == "order.change":
            id = data['id']
            name = data['name']
            schedule = data['schedule']

            sql = "UPDATE `Order` SET name=%s, schedule=%s WHERE id=%s;"
            dbc.execute(sql, [name, schedule, id])
            
        elif route == "order.remove" and check_db_order(id):
            id = data['id']

            sql = "DELETE FROM `Order` WHERE id = %s;"
            dbc.execute(sql, [id])
        
        elif route == "staff.new":
            name = data['name']
            position = data['position']

            sql = "INSERT INTO Staff (name, position) VALUES (%s, %s);"
            dbc.execute(sql, [name, position])
        
        elif route == "staff.change":
            id = data['id']
            name = data['name']
            position = data['position']

            sql = "UPDATE Staff SET name=%s, position=%s WHERE id=%s;"
            dbc.execute(sql, [name, position, id])
            
        elif route == "staff.remove" and check_db_staff(id):
            id = data['id']

            sql = "DELETE FROM Staff WHERE id = %s;"
            dbc.execute(sql, [id])

        db.commit()

        # tampilkan pesan bahwa event sudah diproses
        message = str(event) + ' - ' + str(id)
        logging.warning("Received: %r" % message)

        # acknowledge message dari RabbitMQ secara manual yang 
        # menandakan message telah selesai diproses
        ch.basic_ack(delivery_tag=method.delivery_tag)



    # buka koneksi ke server RabbitMQ di PetraMQ
    credentials = pika.PlainCredentials('radmin', 'rpass')
    connection = pika.BlockingConnection(pika.ConnectionParameters('EOMQ',5672,'/',credentials))
    channel = connection.channel()

    # Buat exchange dan queue
    queue_name = 'event_queue'
    channel.exchange_declare(exchange='EOEX', exchange_type='topic')
    channel.queue_declare(queue=queue_name, exclusive=True)
    channel.queue_bind(exchange='EOEX', queue=queue_name, routing_key='*.new')
    channel.queue_bind(exchange='EOEX', queue=queue_name, routing_key='*.change')
    channel.queue_bind(exchange='EOEX', queue=queue_name, routing_key='*.remove')

    # Ambil message dari RabbitMQ (bila ada)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=get_message)
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)