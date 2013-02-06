#
#  {{ metadata.fileName }}
#  {{ metadata.projectName }}
#
#  Created by {{ metadata.fileAuthor }} on {{ metadata.pubDate }} via Erlenmeyer.
#  Copyright (c) {{ metadata.pubYear }} {{ metadata.projectOwner }}. All rights reserved.
#

# imports
import flask
from models import Model
from flask.ext.sqlalchemy import SQLAlchemy

# globals
settings = json.load(open('settings/settings.json'))

flaskApp = flask.Flask(__name__)
flaskApp.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%(user)s:%(password)s@localhost/%(database)s' % (settings['sql'])

database = SQLAlchemy(flaskApp)

# handlers
{% for model in models %}
# - {{ model.className }}
@flaskApp.route("/{{ model.className }}s", methods = ["GET", "PUT"])
def handle{{ model.className }}s():
    if flask.request.method == "GET":
        return {{ model.className }}Handler.get{{ model.className|capitalize }}s()
        
    elif flask.request.method == "PUT":
        return {{ model.className }}Handler.put{{ model.className|capitalize }}({{ model.primaryKey }}, dict(flask.request.form))
        
@flaskApp.route("/{{ model.className }}s/<{{ model.primaryKey }}>", methods = ["GET", "POST", "DELETE"])
def handle{{ model.className }}({{ model.primaryKey }}):
    if flask.request.method == "GET":
        return {{ model.className }}Handler.get{{ model.className|capitalize }}({{ model.primaryKey }})
        
    elif flask.request.method == "POST":
        return {{ model.className }}Handler.post{{ model.className|capitalize }}({{ model.primaryKey }}, dict(flask.request.form))
        
    elif flask.request.method == "DELETE":
        return {{ model.className }}Handler.delete{{ model.className|capitalize }}({{ model.primaryKey }})
        
{% for relationship in model.relationships %}
# - - {{ relationship.name }}
{% if relationship.isToMany %}
@flaskApp.route("/{{ model.className }}s/<{{ model.primaryKey }}>/{{ relationship.name }}", methods = ["GET", "PUT", "DELETE"])
def handle{{ model.className }}{{ relationship.name|capitalize }}({{ model.primaryKey }}):
    if flask.request.method == "GET":
        return {{ model.className }}Handler.get{{ model.className|capitalize }}{{ relationship.name|capitalize }}({{ model.primaryKey }})
        
    elif flask.request.method == "PUT":
        return {{ model.className }}Handler.put{{ model.className|capitalize }}{{ relationship.name|capitalize }}({{ model.primaryKey }}, flask.request.form['{{ relationship.name }}Object'])
        
    elif flask.request.method == "DELETE":
        return {{ model.className }}Handler.delete{{ model.className|capitalize }}{{ relationship.name|capitalize }}({{ model.primaryKey }}, flask.request.form['{{ relationship.name }}Object'])
        
{% else %}
@flaskApp.route("/{{ model.className }}s/<{{ model.primaryKey }}>/{{ relationship.name }}", methods = ["GET", "POST"])
def handle{{ model.className }}{{ relationship.name|capitalize }}({{ model.primaryKey }}):
    if flask.request.method == "GET":
        return {{ model.className }}Handler.get{{ model.className|capitalize }}{{ relationship.name|capitalize }}({{ model.primaryKey }})
        
    elif flask.request.method == "POST":
        return {{ model.className }}Handler.post{{ model.className|capitalize }}{{ relationship.name|capitalize }}({{ model.primaryKey }}, flask.request.form['{{ relationship.name }}Object'])

{% endif %}
{% endfor %}
{% endfor %}

# main
if __name__ == "__main__":
    Model.database = database

    flaskApp.run(
        host = settings['server']['ip'],
        port = settings['server']['port'],
        debug = settings['server']['debug']
    )