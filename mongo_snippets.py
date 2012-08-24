import os
from sets import Set
from flask import Flask
from flask import render_template

mongo_snippets = Flask(__name__)

SNIPPET_BASE = './snippets'

LANGS = {
  "js": "JavaScript",
  "rb": "Ruby",
  "py": "Python"
}

"""
for category in os.listdir(SNIPPET_BASE):
    category_path = os.path.join(SNIPPET_BASE, category)
    snippet_list = os.listdir(category_path)
    snippet_names = Set([snippet.split('.')[0] for snippet in snippet_list])
    snippets = [' '.join(name.split('_')).title() for name in snippet_names]

    structure[category] = snippets
"""

def path(dirs):
  return os.path.join(SNIPPET_BASE, *dirs)

def make_snippet(category, name):
    snippet = {}
    snippet['languages'] = {}
    for phile in os.listdir(path([category])):
	file_name, ext = phile.split('.')
        if file_name == name:
            data = open(path([category, phile])).read()
            if ext == 'txt':
                snippet['description'] = data
            else:
                lang = LANGS[ext]
	        snippet['languages'][lang] = data

    snippet['name'] = ' '.join(name.split('_')).title()
    return snippet

@mongo_snippets.route("/snippet/<category>/<snippet>")
def show_snippet(category, snippet):
    snippet = make_snippet(category, snippet)
    return render_template("one_snippet.html", snippet=snippet)

@mongo_snippets.route("/<category>/<snippet>")
def index(category, snippet):
    snippet = make_snippet(category, snippet)
    return render_template("index.html", structure={}, snippet=snippet)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    mongo_snippets.debug = True
    mongo_snippets.run(host='0.0.0.0', port=port)
