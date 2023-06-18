import pika, sys

def publish_message(message,route):
    credentials = pika.PlainCredentials('radmin', 'rpass')
    connection = pika.BlockingConnection(pika.ConnectionParameters('EOMQ',5672,'/',credentials))
    channel = connection.channel()

    # Buat exchange baru yang nantinya akan dihubungkan ke satu/lebih queue oleh consumer(s)
    channel.exchange_declare(exchange='EOEX', exchange_type='topic')

    # Kirimkan message ke RabbitMQ
    channel.basic_publish(exchange='EOEX',
                          routing_key=route, 
                          body=message, 
                          properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE) )

    print("Sent a message: " + message)

    connection.close()