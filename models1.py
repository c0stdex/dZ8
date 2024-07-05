from mongoengine import Document, StringField, BooleanField

class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    phone = StringField(required=True)
    preferred_contact_method = StringField(choices=['email', 'sms'])
    message_sent = BooleanField(default=False)
