import pika


def callback(ch, method, properties, body):
    print("AUDITORIA:", body.decode())


connection = pika.BlockingConnection(
    pika.ConnectionParameters("rabbitmq")
)

channel = connection.channel()

channel.queue_declare(queue="fila_viagens")

channel.basic_consume(
    queue="fila_viagens",
    on_message_callback=callback,
    auto_ack=True
)

print("Consumer Auditoria iniciado...")

channel.start_consuming()