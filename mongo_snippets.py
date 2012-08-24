import os
from sets import Set
from flask import Flask
from flask import render_template

mongo_snippets = Flask(__name__)

structure = {}

SNIPPET_BASE = './snippets'

for category in os.listdir(SNIPPET_BASE):
    category_path = os.path.join(SNIPPET_BASE, category)
    snippet_list = os.listdir(category_path)
    snippet_names = Set([snippet.split('.')[0] for snippet in snippet_list])
    snippets = [' '.join(name.split('_')).title() for name in snippet_names]

    structure[category] = snippets

@mongo_snippets.route("/")
def index():
    return render_template("index.html", structure=structure)

if __name__ == "__main__":
    mongo_snippets.debug = True
    mongo_snippets.run()
