import os
from sets import Set
from flask import Flask
from flask import render_template
from pymongo import Connection

mongo_snippets = Flask(__name__)

default_uri = 'mongodb://localhost:27017/snippets'
mongolab_uri = os.env("MONGOLAB_URI", None) or default_uri

conn = Connection(mongolab_uri)
db = conn['snippets']

@mongo_snippets.route('/snippet')
def new_snippet():
    pass

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    mongo_snippets.debug = True
    mongo_snippets.run(host='0.0.0.0', port=port)
