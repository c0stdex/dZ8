import pika
import json
from mongoengine import connect
from models import Contact
from config import MONGODB_URI

connect(host=MONGODB_URI)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue')

def send_email(contact):
    print(f"Sending email to {contact.email}")
    contact.message_sent = True
    contact.save()

def callback(ch, method, properties, body):
    data = json.loads(body)
    contact = Contact.objects(id=data['contact_id']).first()
    if contact:
        send_email(contact)

channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
