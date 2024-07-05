import pika
import json
from mongoengine import connect
from models import Contact
from config import MONGODB_URI

connect(host=MONGODB_URI)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='sms_queue')

def send_sms(contact):
    print(f"Sending SMS to {contact.phone}")
    contact.message_sent = True
    contact.save()

def callback(ch, method, properties, body):
    data = json.loads(body)
    contact = Contact.objects(id=data['contact_id']).first()
    if contact:
        send_sms(contact)

channel.basic_consume(queue='sms_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
