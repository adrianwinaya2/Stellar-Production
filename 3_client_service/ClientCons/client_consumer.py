import pika, sys, os
import mysql.connector,logging, json


db = mysql.connector.connect(host="ClientSQL", user="root", password="root",database="stellar_client")
dbc = db.cursor(dictionary=True)


def main():
    def get_message(ch, method, properties, body):

        # Parse json data di dalam 'body' untuk mengambil data terkait event
        data = json.loads(body)
        username = data['username']
        name = data['name']
        email = data['email']

        # Tambah jumlah order sebanyak 1 untuk id kantin tertentu  
        sql = "INSERT INTO stellar_client (username, name, email) VALUES (%s, %s, %s);"
        dbc.execute(sql, [username, name, email])
        db.commit()

        # tampilkan pesan bahwa event sudah diproses
        message = str(username) + ' - ' + str(name) + '-' + str(email)
        logging.warning("Client added : %r" % message)

        # acknowledge message dari RabbitMQsecara manual yang 
        # menandakan message telah selesai diproses
        ch.basic_ack(delivery_tag=method.delivery_tag)



    # buka koneksi ke server RabbitMQ di PetraMQ
    credentials = pika.PlainCredentials('radmin', 'rpass')
    connection = pika.BlockingConnection(pika.ConnectionParameters('EOMQ',5672,'/',credentials))
    channel = connection.channel()

    # Buat exchange dan queue
    queue_name = 'client_consumer'
    channel.exchange_declare(exchange='EOEX', exchange_type='topic')
    channel.queue_declare(queue=queue_name, exclusive=True) 

    # Ambil message dari RabbitMQ (bila ada)
    channel.queue_bind(exchange='EOEX', queue=queue_name, routing_key='client.new')
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