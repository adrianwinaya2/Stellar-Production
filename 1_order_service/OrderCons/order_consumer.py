import pika, sys, os
import mysql.connector,logging, json


db = mysql.connector.connect(host="OrderSQL", user="root", password="root",database="stellar_order")
dbc = db.cursor(dictionary=True)


def main():
    def check_db_client(id):
        sql = "SELECT * FROM Client WHERE id = %s"
        dbc.execute(sql, [id])
        client = dbc.fetchone()
        return True if client else False
    
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

        if route == "client.new":
            name = data['name']
            email = data['email']
            
            sql = "INSERT INTO Client (name, email) VALUES (%s, %s);"
            dbc.execute(sql, [name, email])

        elif route == "client.change":
            name = data['name']
            email = data['email']
            id = data['id']
            
            sql = "UPDATE Client SET name=%s, email=%s WHERE id=%s;"
            dbc.execute(sql, [name, email, id])

        elif route == "client.remove":
            id = data['id']
            if check_db_client(id):
                sql = "DELETE FROM Client WHERE id = %s"
                dbc.execute(sql, [id])
        
        elif route == "staff.new":
            name = data['name']
            position = data['position']

            sql = "INSERT INTO Staff (name, position) VALUES (%s, %s);"
            dbc.execute(sql, [name, position])
        
        elif route == "staff.change":
            name = data['name']
            position = data['position']
            id = data['id']

            sql = "UPDATE Staff SET name=%s, position=%s WHERE id=%s;"
            dbc.execute(sql, [name, position, id])
        
        elif route == "staff.remove":
            id = data['id']

            if check_db_staff(id):
                sql = "DELETE FROM Staff WHERE id = %s"
                dbc.execute(sql, [id])

        db.commit()

        # tampilkan pesan bahwa event sudah diproses
        message = str(event)
        logging.warning("Received: %r" % message)

        # acknowledge message dari RabbitMQ secara manual yang 
        # menandakan message telah selesai diproses
        ch.basic_ack(delivery_tag=method.delivery_tag)



    # buka koneksi ke server RabbitMQ di PetraMQ
    credentials = pika.PlainCredentials('radmin', 'rpass')
    connection = pika.BlockingConnection(pika.ConnectionParameters('EOMQ',5672,'/',credentials))
    channel = connection.channel()

    # Buat exchange dan queue
    queue_name = 'order_queue'
    channel.exchange_declare(exchange='EOEX', exchange_type='topic')
    channel.queue_declare(queue=queue_name, exclusive=True)
    channel.queue_bind(exchange='EOEX', queue=queue_name, routing_key='client.*')
    channel.queue_bind(exchange='EOEX', queue=queue_name, routing_key='staff.*')

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