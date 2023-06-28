import pika, sys, os
import mysql.connector,logging, json


db = mysql.connector.connect(host="AccountSQL", user="root", password="root",database="stellar_account")
dbc = db.cursor(dictionary=True)


def main():
    def get_message(ch, method, properties, body):
        route = method.routing_key
        
        # Parse json data di dalam 'body' untuk mengambil data terkait event
        data = json.loads(body)
        event = data['event']
        id = data['id']
        username = data['username']

        # Tambah jumlah order sebanyak 1 untuk id kantin tertentu
        if route == '*.change':
            sql = "UPDATE Account SET username=%s WHERE username=%s;"
            dbc.execute(sql, [username, username] )
        elif route == '*.remove':
            sql = "DELETE FROM Account WHERE username=%s;"
            dbc.execute(sql, [username] )

        db.commit()

        # tampilkan pesan bahwa event sudah diproses
        message = 'id: ' + str(id) + ' - username: ' + str(username)
        logging.warning("%r : %r" % str(event), message)
        
        # acknowledge message dari RabbitMQsecara manual yang 
        # menandakan message telah selesai diproses
        ch.basic_ack(delivery_tag=method.delivery_tag)



    # buka koneksi ke server RabbitMQ di PetraMQ
    credentials = pika.PlainCredentials('radmin', 'rpass')
    connection = pika.BlockingConnection(pika.ConnectionParameters('EOMQ',5672,'/',credentials))
    channel = connection.channel()

    # Buat exchange dan queue
    queue_name = 'account_queue'
    channel.exchange_declare(exchange='EOEX', exchange_type='topic')
    channel.queue_declare(queue=queue_name, exclusive=True)
    channel.queue_bind(exchange='EOEX', queue=queue_name, routing_key='client.change')
    channel.queue_bind(exchange='EOEX', queue=queue_name, routing_key='staff.change')
    channel.queue_bind(exchange='EOEX', queue=queue_name, routing_key='client.remove')
    channel.queue_bind(exchange='EOEX', queue=queue_name, routing_key='staff.remove')

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