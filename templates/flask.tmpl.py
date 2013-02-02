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
{% for model in models -%}
import {{ model.className }}
{% endfor %}

# globals
flaskApp = flask.Flask(__name__)
settings = json.load(open('../settings/settings.json'))

# handlers
{% for model in models -%}
#  {{ model.className }}
@app.route("/{{ model.className|lower }}s/", methods = ["GET", "PUT"])
def handle{{ model.className|capitalize }}s():
    if flask.request.method == "GET":
        all{{ model.className }}s = {{ model.className }}.{{ model.className }}.all()
        all{{ model.className }}sDictionaries = [dict({{ model.className|lower }}) for {{ model.className|lower }} in all{{ model.className }}s]
        
        return flask.Response(
            json.dumps(all{{ model.className }}sDictionaries),
            200, 'application/json'
        )
    
    elif flask.request.method == "PUT":
        pass
    
@app.route("/{{ model.className|lower }}s/<{{ model.primaryKey }}>", methods = ["GET", "POST", "DELETE"])
def handle{{ model.className|capitalize }}({{ model.primaryKey}}):
    if flask.request.method == "GET":
        {{ model.className|lower }}s = {{ model.className }}.{{ model.className }}.all({{ model.primaryKey }} = {{ model.primaryKey }})
        if not {{ model.className|lower }}s:
            return flask.Response(
                '', 404, 'application/json'
            )
            
        {{ model.className|lower }}Dictionary = dict({{ model.className|lower }}s[0])
        
        return flask.Response(
            json.dumps({{ model.className|lower }}Dictionary),
            200, 'application/json'
        )
        
    elif flask.request.method == "POST":
        pass

    elif flask.request.method == "DELETE":
        pass
    
{% for attribute in model.attributes if attribute.name != model.primaryKey -%}
#   {{ attribute.name }}
@app.route("/{{ model.className|lower }}s/<{{ model.primaryKey }}>/{{ attribute.name }}", methods = ["GET", "POST"])
def handle{{ model.className|capitalize }}{{ attribute.name|capitalize }}({{ model.primaryKey }}):
    if flask.request.method == "GET":
        {{ model.className|lower }}s = {{ model.className }}.{{ model.className }}.all({{ model.primaryKey }} = {{ model.primaryKey }})
        if not {{ model.className|lower }}s:
            return flask.Response(
                '', 404, 'application/json'
            )
            
        {{ model.className|lower }} = {{ model.className|lower }}s[0]
        {{ attribute.name }} = {{ model.className|lower }}.{{ attribute.name }}
        
        return flask.Response(
            json.dumps({{ attribute.name }}),
            200, 'application/json'
        )
        
    elif flask.request.method == "POST":
        pass
    
{% endfor %}

{%- for relationship in model.relationships -%}
#   {{ relationship.name }}
{% if relationship.toMany -%}
@app.route("/{{ model.className|lower }}s/<{{ model.primaryKey }}>/{{ relationship.name }}", methods = ["GET", "PUT", "DELETE"])
def handle{{ model.className|capitalize }}{{ relationship.name|capitalize }}({{ model.primaryKey }}):
    if flask.request.method == "GET":
        {{ model.className|lower }}s = {{ model.className }}.{{ model.className }}.all({{ model.primaryKey }} = {{ model.primaryKey }})
        if not {{ model.className|lower }}s:
            return flask.Response(
                '', 404, 'application/json'
            )
            
        {{ model.className|lower }} = {{ model.className|lower }}s[0]
        {{ relationship.name }} = {{ relationship.type }}.{{ relationship.type }}.all({{ model.className|lower }} = {{ model.className|lower }}.{{ relationship.name }})
        
        if not {{ relationship.name }}:
            return flask.Response(
                '', 204, 'application/json'
            )
            
        {{ relationship.type|lower }}Dictionaries = [dict({{ relationship.type|lower }}) for {{ relationship.type|lower }} in {{ relationship.name }}]
        
        return flask.Response(
            json.dumps({{ relationship.type|lower }}Dictionaries),
            200, 'application/json'
        )
        
    elif flask.request.method == "PUT":
        pass
        
    elif flask.request.method == "DELETE":
        pass
{%- else -%}
@app.route("/{{ model.className|lower }}s/<{{ model.primaryKey }}>/{{ relationship.name }}", methods = ["GET", "POST"])
def handle{{ model.className|capitalize }}{{ relationship.name|capitalize }}({{ model.primaryKey }}):
    if flask.request.method == "GET":
        {{ model.className|lower }}s = {{ model.className }}.{{ model.className }}.all({{ model.primaryKey }} = {{ model.primaryKey }})
        if not {{ model.className|lower }}s:
            return flask.Response(
                '', 404, 'application/json'
            )
            
        {{ model.className|lower }} = {{ model.className|lower }}s[0]
        {{ relationship.name }}s = {{ relationship.type }}.{{ relationship.type }}.all({{ model.primaryKey }} = {{ model.className|lower }}.{{ relationship.name }})
        
        if not {{ relationship.name }}s:
            return flask.Response(
                '', 204, 'application/json'
            )
            
        {{ relationship.name }}Dictionary = dict({{ relationship.name }}s[0])
        
        return flask.Response(
            json.dumps({{ relationship.name }}Dictionary),
            200, 'application/json'
        )
        
    elif flask.request.method == "POST":
        pass
{%- endif %}
{%- endfor %}
{% endfor %}

if __name__ == "__main__":
    flaskApp.run(
        host = settings["server"]["ip"],
        port = settings["server"]["port"],
        debug = settings["server"]["debug"]
    )