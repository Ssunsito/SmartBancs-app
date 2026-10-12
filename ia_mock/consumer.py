import pika
import json
import time
import os

# Lee la URL inyectada por Docker Compose. Si no existe, usa localhost como respaldo.
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://admin:admin123@localhost:5672/")

def procesar_ia(ch, method, properties, body):
    payload = json.loads(body)
    tx_id = payload.get("transaccion_id")
    print(f"[IA-Mock] Iniciando inferencia para la transacción: {tx_id}")
    
    # Simula el tiempo de procesamiento de un modelo de IA (Ej: Red Neuronal)
    time.sleep(1.5) 
    
    recomendacion = "Sugerencia de inversión en fondo de bajo riesgo" if payload.get("monto") > 100 else "Ahorro programado"
    print(f"[IA-Mock] Inferencia completada para {tx_id}. Recomendación generada: {recomendacion}")
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    print(f"[IA-Mock] Conectando al broker en: {RABBITMQ_URL}")
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()
    channel.queue_declare(queue="cola_inferencia_ia", durable=True)
    
    print("[IA-Mock] Esperando eventos de inferencia de IA...")
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="cola_inferencia_ia", on_message_callback=procesar_ia)
    channel.start_consuming()

if __name__ == "__main__":
    # Pequeña pausa inicial para asegurar que RabbitMQ esté completamente listo antes de conectar
    time.sleep(5)
    main()