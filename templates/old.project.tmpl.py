#
#  {{ metadata.fileName }}
#  {{ metadata.projectName }}
#
#  Created by {{ metadata.fileAuthor }} on {{ metadata.pubDate }} via Erlenmeyer.
#  Copyright (c) {{ metadata.pubYear }} {{ metadata.projectOwner }}. All rights reserved.
#

# imports
import json
import flask
{% for model in models -%}
from handlers import {{ model.className }}Handler
{% endfor %}

# globals
flaskApp = flask.Flask(__name__)
settings = json.load('../settings/settings.json')

# handlers
{% for model in models -%}
# - {{ model.className }}
@flaskApp.route("/{{ model.className|lower }}s", methods = ["GET", "PUT"])
def handle{{ model.className|capitalize }}s():
    if flask.request.method == "GET":
        return {{ model.className }}Handler.get{{ model.className|capitalize }}s()
        
    elif flask.request.method == "PUT":
        return {{ model.className }}Handler.put{{ model.className|capitalize }}(dict(flask.request.form))
        
@flaskApp.route("/{{ model.className|lower }}s/<{{ model.primaryKey }}>", method = ["GET", "POST", "DELETE"])
def handle{{ model.className|capitalize }}({{ model.primaryKey }}):
    if flask.request.method == "GET":
        return {{ model.className }}Handler.get{{ model.className|capitalize }}({{ model.primaryKey }})
        
    elif flask.request.method == "POST":
        return {{ model.className }}Handler.post{{ model.className|capitalize }}({{ model.primaryKey }}, dict(flask.request.form))
        
    elif flask.request.method == "DELETE":
        return {{ model.className }}Handler.delete{{ model.className|capitalize }}({{ model.primaryKey }})
        
{% for attribute in model.attributes if attribute.name != model.primaryKey -%}
# - - {{ attribute.name }}
@flaskApp.route("/{{ model.className|lower }}s/<{{ model.primaryKey }}>/{{ attribute.name }}", methods = ["GET", "POST"])
def handle{{ model.className|capitalize }}{{ attribute.name|capitalize }}({{ model.primaryKey }}):
    if flask.request.method == "GET":
        return {{ model.className }}Handler.get{{ model.className|capitalize }}{{ attribute.name|capitalize }}({{ model.primaryKey }})
        
    elif flask.request.method == "POST":
        return {{ model.className }}Handler.post{{ model.className|capitalize }}{{ attribute.name|capitalize }}({{ model.primaryKey }}, flask.request.form["{{ attribute.name }}"])
{% endfor %}

{%- for relationship in model.relationships -%}
# - - {{ relationship.name }}
{% if relationship.toMany -%}
@flaskApp.route("/{{ model.className|lower }}s/<{{ model.primarKey }}>/{{ relationship.name }}", methods = ["GET", "POST", "DELETE"])
def handle{{ model.className|capitalize }}{{ relationship.name|capitalize }}({{ model.primaryKey }}):
    if flask.request.method == "GET":
        return {{ model.className }}Handler.get{{ model.className|capitalize }}{{ relationship.name|capitalize }}({{ model.primaryKey }})
        
    elif flask.request.method == "POST":
        return {{ model.className }}Handler.post{{ model.className|capitalize }}{{ relationship.name|capitalize }}({{ model.primaryKey }}, flask.request.form["{{ relationship.name }}{{ model.primaryKey|capitalize }}"])
        
    elif flask.request.method == "DELETE":
        return {{ model.className }}Handler.delete{{ model.className|capitalize }}{{ relationship.name|capitalize }}({{ model.primaryKey }}, flask.request.form["{{ relationship.name }}{{ model.primaryKey|capitalize }}"])
        
{%- else -%}
@flaskApp.route("/{{ model.className|lower }}s/<{{ model.primaryKey }}>/{{ relationship.name }}", methods = ["GET", "POST"])
def handle{{ model.className|capitalize }}{{ relationship.name|capitalize }}({{ model.primaryKey }}):
    if flask.request.method == "GET":
        return {{ model.className }}Handler.get{{ model.className|capitalize }}{{ relationship.name|capitalize }}({{ model.primaryKey }})
        
    elif flask.request.method == "POST":
        return {{ model.className }}Handler.delete{{ model.className|capitalize }}{{ relationship.name|capitalize }}({{ model.primaryKey }}, flask.request.form["{{ relationship.name }}{{ model.primaryKey|capitalize }}"])
        
{%- endif %}
{%- endfor %}
{% endfor %}

# main
if __name__ == "__main__":
    flaskApp.run(
        host = settings['server']['ip'],
        port = settings['server']['port'],
        debug = settings['server']['debug']
    )