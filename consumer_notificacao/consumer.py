import pika


def callback(ch, method, properties, body):
    print("NOTIFICACAO:", body.decode())


connection = pika.BlockingConnection(
    pika.ConnectionParameters("rabbitmq")
)

channel = connection.channel()

channel.queue_declare(queue="fila_notificacoes")

channel.basic_consume(
    queue="fila_notificacoes",
    on_message_callback=callback,
    auto_ack=True
)

print("Consumer Notificação iniciado...")

channel.start_consuming()