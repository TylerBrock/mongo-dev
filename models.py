import settings
from pymongo import Connection

conn = Connection(settings.MONGO_URI)
db = conn['mongo-dev']
snippets = db['snippets']
users = db['users']

class User:
    def __init__(self, data):
        self.data = data

    def save(self):
        users.insert(self.data)

class Snippet:
    pass
