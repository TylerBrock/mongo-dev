import os
from sets import Set
from flask import Flask
from flask import render_template, request, redirect, url_for
from pymongo import Connection
from bson import ObjectId

mongo_snippets = Flask(__name__)

default_uri = 'mongodb://localhost:27017/snippets'
mongolab_uri = os.environ.get("MONGOLAB_URI", None) or default_uri

conn = Connection(mongolab_uri)
db = conn['mongo-snippets']
snippets = db['snippets']

langs = [ "C", "C#", "C++", "Java", "NodeJS",
          "MongoShell", "Perl", "PHP",
           "Python", "Ruby", "Scala", "Go"]

@mongo_snippets.route('/snippet/all', methods=['GET','POST'])
def all_snippets():
    all_groups = [d for d in db.snippets.aggregate({"$group":{"_id":{"name":"$name"}, "langs":{"$addToSet":"$lang"}}})['result']]
    print all_groups
    return render_template("all_groups.html", groups=all_groups)

@mongo_snippets.route('/snippet', methods=['GET','POST'])
def new_snippet():
    error = None
    if request.method == 'POST':
        code = request.form.get('snippet_code', "")
        lang = request.form.get('language', "")
        name = request.form.get('name', "")
        desc = request.form.get('description', "")
        #TODO validate language, name, description
        snippet = dict(code=code, lang=lang, name=name, desc=desc)
        oid = snippets.insert(snippet, safe=True)
        return redirect(url_for("show_snippet", snip_id=str(oid)))
    else:
        return render_template('create_snippet.html', langs=langs)

@mongo_snippets.route('/snippet/<snip_id>', methods=['GET','POST'])
def show_snippet(snip_id):
    try:
        snip_id_oid = ObjectId(snip_id)
    except:
        snip_id_oid = None

    if not snip_id_oid:
        abort(404)

    snippet = snippets.find_one({"_id" : snip_id_oid})
    if not snippet:
        abort(404)
    else:
        return render_template("snippet.html", snippet=snippet)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    mongo_snippets.debug = True
    mongo_snippets.run(host='0.0.0.0', port=port)
