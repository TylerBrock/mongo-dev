import requests
import json
import settings
from pymongo import Connection

conn = Connection(settings.MONGO_URI)
db = conn['mongo-dev']
snippets = db['snippets']
users = db['users']

class User:
	def __init__(self, code):
		pass

class Snippet:
    pass
