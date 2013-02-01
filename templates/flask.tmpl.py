#
#  {{ metadata.fileName }}
#  {{ metadata.projectName }}
#
#  Created by {{ metadata.fileAuthor }} on {{ metadata.pubDate }}.
#  Copyright (c) {{ metadata.pubYear }} {{ metadata.projectOwner }}. All rights reserved.
#

# imports
import flask
import json
import models

# globals
flaskApp = flask.Flask(__name__)
settings = json.load(open('../settings/settings.json'))

# handlers
{% for model in models -%}
#  {{ model.className }}
@app.route("/{{ model.className|lower }}s/", methods = ["GET", "PUT"])
def handle{{ model.className|capitalize }}s():
    if flask.request.method == "GET":
        pass
        
    elif flask.request.method == "PUT":
        pass
    
@app.route("/{{ model.className|lower }}s/<{{ model.primaryKey }}>", methods = ["GET", "POST", "DELETE"])
def handle{{ model.className|capitalize }}({{ model.primaryKey}}):
    if flask.request.method == "GET":
        pass
        
    elif flask.request.method == "POST":
        pass

    elif flask.request.method == "DELETE":
        pass
    
{% for attribute in model.attributes if attribute.name != model.primaryKey -%}
#   {{ attribute.name }}
@app.route("/{{ model.className|lower }}s/<{{ model.primaryKey }}>/{{ attribute.name }}", methods = ["GET", "POST"])
def handle{{ model.className|capitalize }}{{ attribute.name|capitalize }}({{ model.primaryKey }}):
    if flask.request.method == "GET":
        pass
        
    elif flask.request.method == "POST":
        pass
    
{% endfor %}

{%- for relationship in model.relationships -%}
#   {{ relationship.name }}
{% if relationship.toMany -%}
@app.route("/{{ model.className|lower }}s/<{{ model.primaryKey }}>/{{ relationship.name }}", methods = ["GET", "PUT", "DELETE"])
def handle{{ model.className|capitalize }}{{ relationship.name|capitalize }}({{ model.primaryKey }}):
    if flask.request.method == "GET":
        pass
        
    elif flask.request.method == "PUT":
        pass
        
    elif flask.request.method == "DELETE":
        pass
{%- else -%}
@app.route("/{{ model.className|lower }}s/<{{ model.primaryKey }}>/{{ relationship.name }}", methods = ["GET", "POST"])
def handle{{ model.className|capitalize }}{{ relationship.name|capitalize }}({{ model.primaryKey }}):
    if flask.request.method == "GET":
        pass
        
    elif flask.request.method == "POST":
        pass
{%- endif %}
{%- endfor %}
{% endfor %}

if __name__ == "__main__":
    flaskApp.run(
        
    )