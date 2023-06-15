import pika, sys, os
import mysql.connector,logging, json


db = mysql.connector.connect(host="KantinSQL", user="root", password="root",database="soa_db")
dbc = db.cursor(dictionary=True)


def main():
    def get_message(ch, method, properties, body):

        # Parse json data di dalam 'body' untuk mengambil data terkait event
        data = json.loads(body)
        event = data['event']
        kantin_id = data['kantin_id']

        # Tambah jumlah order sebanyak 1 untuk id kantin tertentu  
        sql = "update kantin_resto set jmlorder=jmlorder+1 WHERE id=%s"
        dbc.execute(sql, [kantin_id] )
        db.commit()

        # tampilkan pesan bahwa event sudah diproses
        message = str(event) + ' - ' + str(kantin_id)
        logging.warning("Received: %r" % message)

        # acknowledge message dari RabbitMQsecara manual yang 
        # menandakan message telah selesai diproses
        ch.basic_ack(delivery_tag=method.delivery_tag)



    # buka koneksi ke server RabbitMQ di PetraMQ
    credentials = pika.PlainCredentials('radmin', 'rpass')
    connection = pika.BlockingConnection(pika.ConnectionParameters('PetraMQ',5672,'/',credentials))
    channel = connection.channel()

    # Buat exchange dan queue
    channel.exchange_declare(exchange='PetraEX', exchange_type='topic')
    new_queue = channel.queue_declare(queue='', exclusive=True)
    new_queue_name = new_queue.method.queue
    channel.queue_bind(exchange='PetraEX', queue=new_queue_name, routing_key='order.new')

    # Ambil message dari RabbitMQ (bila ada)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=new_queue_name, on_message_callback=get_message)
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