import pika
import json
from faker import Faker
from mongoengine import connect
from models import Contact
from config import MONGODB_URI

fake = Faker()
connect(host=MONGODB_URI)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue')
channel.queue_declare(queue='sms_queue')

def create_contacts(n):
    for _ in range(n):
        contact = Contact(
            fullname=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            preferred_contact_method=fake.random_element(elements=('email', 'sms'))
        ).save()
        message = {
            'contact_id': str(contact.id),
            'preferred_contact_method': contact.preferred_contact_method
        }
        queue = 'email_queue' if contact.preferred_contact_method == 'email' else 'sms_queue'
        channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(message))

create_contacts(10)
connection.close()
