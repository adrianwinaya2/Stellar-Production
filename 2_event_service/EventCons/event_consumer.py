import pika, sys, os
import mysql.connector,logging, json


# db = mysql.connector.connect(host="OrderSQL", user="root", password="root",database="soa_db")
# dbc = db.cursor(dictionary=True)


def main():
    def get_message(ch, method, properties, body):

        # Parse json data di dalam 'body' untuk mengambil data terkait event
        data = json.loads(body)
        event = data['event']
        kantin_id = data['id']

        # tampilkan pesan bahwa event sudah diproses
        message = str(event) + ' - ' + str(kantin_id)
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