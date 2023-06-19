import pika, sys, os
import mysql.connector,logging, json


db = mysql.connector.connect(host="OrderSQL", user="root", password="root",database="soa_db")
dbc = db.cursor(dictionary=True)


def main():
    def check_db(id):
        sql = "SELECT * FROM Client WHERE id = %s"
        dbc.execute(sql, [id])
        client = dbc.fetchone()
        return True if client else False

    def get_message(ch, method, properties, body):

        # Parse json data di dalam 'body' untuk mengambil data terkait event
        route = method.routing_key
        data = json.loads(body)
        event = data['event']
        id = data['id']

        if route == "client.change":
            name = data['name']
            email = data['email']
            
            sql = "INSERT INTO stellar_client (username, name, email) VALUES (%s, %s);"
            dbc.execute(sql, [name, email])

        elif route == "client.remove" and check_db(id):
            sql = "DELETE FROM Client WHERE id = %s"
            dbc.execute(sql, [id])
        
        elif route == "staff.change":
            name = data['name']
            position = data['position']

            sql = "INSERT INTO stellar_staff (name, position) VALUES (%s, %s);"
            dbc.execute(sql, [name, email])
        
        elif route == "staff.remove" and check_db(id):
            sql = "DELETE FROM Staff WHERE id = %s"
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
    queue_name = 'order_queue'
    channel.exchange_declare(exchange='EOEX', exchange_type='topic')
    channel.queue_declare(queue=queue_name, exclusive=True)
    channel.queue_bind(exchange='EOEX', queue=queue_name, routing_key=['client.*', 'staff.*'])

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