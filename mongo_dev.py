import os
import requests
import json
import settings
from sets import Set
from flask import Flask
from flask import render_template, request, redirect, url_for
from pymongo import Connection
from bson import ObjectId

mongo_dev = Flask(__name__)

conn = Connection(settings.MONGO_URI)
db = conn['mongo-dev']
snippets = db['snippets']
users = db['users']

def get_user(access_token):
    params = {"access_token": access_token}
    user = requests.get(settings.GH_API_URL + 'user', params=params, headers=settings.ACCEPT_HEADERS)
    return user

@mongo_dev.route('/register')
def register():
    return redirect(settings.GH_AUTHORIZE_URL)

@mongo_dev.route('/link')
def link():
    code = request.args.get('code', None)
    if code:
        data = {
            "client_id": settings.GH_CLIENT_ID,
            "client_secret": settings.GH_CLIENT_SECRET,
            "code": code
        }
        response = requests.post(
            settings.GH_ACCESS_TOKEN_URL,
            data=data,
            headers=settings.ACCEPT_HEADERS
        )
        token = json.loads(response.text)['access_token']
        user = get_user(token)
        return user.content

@mongo_dev.route('/snippet/all', methods=['GET','POST'])
def all_snippets():
    all_groups = [d for d in db.snippets.aggregate({"$group":{"_id":{"name":"$name"}, "langs":{"$addToSet":"$lang"}}})['result']]
    print all_groups
    return render_template("all_groups.html", groups=all_groups)

@mongo_dev.route('/snippet', methods=['GET','POST'])
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
        return render_template('create_snippet.html', langs=settings.LANGS)

@mongo_dev.route('/snippet/<snip_id>', methods=['GET','POST'])
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
    mongo_dev.debug = True
    mongo_dev.run(host='0.0.0.0', port=port)
