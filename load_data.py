import json
from mongoengine import connect
from models import Author, Quote
from config import MONGODB_URI

connect(host=MONGODB_URI)

with open('authors.json') as f:
    authors_data = json.load(f)

with open('quotes.json') as f:
    quotes_data = json.load(f)

for author_data in authors_data:
    author = Author(**author_data).save()

for quote_data in quotes_data:
    author = Author.objects(fullname=quote_data['author']).first()
    quote_data['author'] = author
    Quote(**quote_data).save()
