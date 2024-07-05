import redis
from mongoengine import connect
from models import Quote
from config import MONGODB_URI, REDIS_HOST, REDIS_PORT

connect(host=MONGODB_URI)
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

def search_quotes_by_author(name):
    cached_result = redis_client.get(f"author:{name}")
    if cached_result:
        return cached_result.decode('utf-8')
    quotes = Quote.objects(author__fullname__icontains=name)
    result = "\n".join([quote.quote for quote in quotes])
    redis_client.set(f"author:{name}", result)
    return result

def search_quotes_by_tags(tags):
    tags_list = tags.split(',')
    cached_result = redis_client.get(f"tags:{tags}")
    if cached_result:
        return cached_result.decode('utf-8')
    quotes = Quote.objects(tags__in=tags_list)
    result = "\n".join([quote.quote for quote in quotes])
    redis_client.set(f"tags:{tags}", result)
    return result

while True:
    command = input("Enter command: ")
    if command.startswith("name:"):
        name = command[len("name:"):].strip()
        print(search_quotes_by_author(name))
    elif command.startswith("tag:"):
        tag = command[len("tag:"):].strip()
        print(search_quotes_by_tags(tag))
    elif command.startswith("tags:"):
        tags = command[len("tags:"):].strip()
        print(search_quotes_by_tags(tags))
    elif command == "exit":
        break
