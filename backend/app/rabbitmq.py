import json
import pika


def publicar_mensagem(fila: str, mensagem: dict):

    connection = pika.BlockingConnection(
        pika.ConnectionParameters("rabbitmq")
    )

    channel = connection.channel()

    channel.queue_declare(queue=fila)

    channel.basic_publish(
        exchange="",
        routing_key=fila,
        body=json.dumps(mensagem)
    )

    connection.close()