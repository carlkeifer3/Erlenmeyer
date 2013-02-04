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
from models import {{ model.className }}

# handlers
def get{{ model.className|capitalize }}s():
    """
    Returns a list of all {{ model.className }}s.
    
    @return: A flask response built with a JSON list of all {{ model.className }}s.
    """
    
    all{{ model.className|capitalize }}s = {{ model.className }}.{{ model.className }}.all()
    all{{ model.className|capitalize }}sDictionaries = [dict({{ model.className|lower }}) for {{ model.className|lower }} in all{{ model.className|capitalize }}s]
    
    return flask.Response(
        response = json.dumps(all{{ model.className|capitalize }}sDictionaries),
        status = 200,
        content_type = 'application/json'
    )
    
def put{{ model.className|capitalize }}({{ model.className|lower }}Dictionary):
    """
    Inserts a new {{ model.className }} with the given properties into the database.
    
    @param {{ model.className|lower }}Dictionary: A series of key-value pairs to apply to the new {{ model.className }}.
    
    @return: An empty flask response.
    """
    
    {{ model.className|lower }} = {{ model.className }}.{{ model.className }}(properties = {{ model.className|lower }}Dictionary)
    {{ model.className|lower }}.save()
    
    return flask.Response(
        response = '',
        status = 200,
        content_type = 'application/json'
    )
    
def get{{ model.className|capitalize }}({{ model.primaryKey }}):
    """
    Returns the {{ model.className }} with the given {{ model.primaryKey }}.
    
    @param {{ model.primaryKey }}: The {{ model.primaryKey }} identifying the desired {{ model.className }}.
    
    @return: An empty flask response with status 404 if the desired {{ model.className }} cannot be found. A flask response built with the JSON dictionary for the desired {{ model.className }} otherwise.
    """
    
    {{ model.className|lower }} = {{ model.className }}.{{ model.className }}.modelFor{{ model.primaryKey }}({{ model.primaryKey }})
    if not {{ model.className|lower }}:
        return flask.Response(
            resposne ='',
            status = 404,
            content_type = 'application/json'
        )
        
    {{ model.className|lower }}Dictionary = dict({{ model.className|lower }})
    
    return flask.Response(
        response = json.dumps({{ model.className|lower }}Dictionary),
        status = 200,
        content_type = 'application/json'
    )
    
def post{{ model.className|capitalize }}({{ model.primaryKey }}, {{ model.className|lower }}Dictionary):
    """
    Updates the {{ model.className }} with the given {{ model.primaryKey }} to have the given properties.
    
    @param {{ model.primaryKey }}: The {{ model.primaryKey }} identifying the desired {{ model.className }}.
    @param {{ model.className|lower }}Dictionary: A series of key-value pairs to apply to the desired {{ model.className }}.
    
    @return: An empty flask response with status 404 if the desired {{ model.className }} cannot be found. An empty flask response with status 200 otherwise.
    """
    
    {{ model.className|lower }} = {{ model.className }}.{{ model.className }}.modelFor{{ model.primaryKey }}({{ model.primaryKey }})
    if not {{ model.className|lower }}:
        return flask.Response(
            resposne ='',
            status = 404,
            content_type = 'application/json'
        )
        
    {{ model.className|lower }}._applyProperties({{ model.className|lower }}Dictionary)
    {{ model.className|lower }}.save()
    
    return flask.Response(
        response = '',
        status = 200,
        content_type = 'application/json'
    )
    
def delete{{ model.className|capitalize }}({{ model.primaryKey }}):
    """
    Deletes the {{ model.className }} with the given {{ model.primaryKey }}.
    
    @param {{ model.primarKey }}: The {{ model.primaryKey }} identifying the desired {{ model.className }}.
    
    @return: An empty flask reponse with status 404 if the desired {{ model.className }} cannot be found. An empty flask response with status 200 otherwise.
    """
    
    {{ model.className|lower }} = {{ model.className }}.{{ model.className }}.modelFor{{ model.primaryKey }}({{ model.primaryKey }})
    if not {{ model.className|lower }}:
        return flask.Response(
            resposne ='',
            status = 404,
            content_type = 'application/json'
        )
        
    {{ model.className|lower }}.delete()
    
    return flask.Response(
        response = '',
        status = 200,
        content_type = 'application/json'
    )
    
# - attributes
{% for attribute model.attributes if attribute.name != model.primaryKey -%}
def get{{ model.className|capitalize }}{{ attribute.name|capitalize }}({{ model.primaryKey }}):
    """
    Returns the {{ attribute.name }} of the {{ model.className }} with the given {{ model.primaryKey }}.
    
    @param {{ model.primaryKey }}: The {{ model.primaryKey }} identifying the desired {{ model.className }}.
    
    @return: An empty flask reponse with status 404 if the desired {{ model.className }} cannot be found. A flask response with the JSON representation of the {{ attribute.name }} of the desired {{ model.className }}.
    """
    
    {{ model.className|lower }} = {{ model.className }}.{{ model.className }}.modelFor{{ model.primaryKey }}({{ model.primaryKey }})
    if not {{ model.className|lower }}:
        return flask.Response(
            resposne ='',
            status = 404,
            content_type = 'application/json'
        )
    
    {{ attribute.name }} = {{ model.className|lower }}.{{ attribute.name }}
    
    return flask.Response(
        response = json.dumps({{ attribute.name }}),
        status = 200,
        content_type = 'application/json'
    )
    
def post{{ model.className|capitalize }}{{ attribute.name|capitalize }}({{ model.primaryKey }}, {{ attribute.name }}):
    """
    Sets the {{ attribute.name }} of the {{ model.className }} with the given {{ model.primaryKey }} to the given value.
    
    @param {{ model.primaryKey }}: The {{ model.primaryKey }} identifying the desired {{ model.className }}.
    @param {{ attribute.name }}: The desired value of the {{ model.className }}'s {{ attribute.name }}.
    
    @return: An empty flask reponse with status 404 if the desired {{ model.className }} cannot be found. An empty flask response with status 200 otherwise.
    """
    
    {{ model.className|lower }} = {{ model.className }}.{{ model.className }}.modelFor{{ model.primaryKey }}({{ model.primaryKey }})
    if not {{ model.className|lower }}:
        return flask.Response(
            resposne ='',
            status = 404,
            content_type = 'application/json'
        )
        
    {{ model.className|lower }}.{{ attribute.name }} = {{ attribute.name }}
    {{ model.className|lower }}.save()
    
    return flask.Response(
        response = '',
        status = 200,
        content_type = 'application/json'
    )
    
{% endfor -%}

# - relationships
{% for relationship in model.relationships -%}
{% if relationship.toMany -%}
def get{{ model.className|capitalize }}{{ relationship.name|capitalize }}({{ model.primaryKey }}):
    """
    Returns the {{ relationship.name }} of the {{ model.className }} with the given {{ model.primaryKey }}.
    
    @param {{ model.primaryKey }}: The {{ model.primaryKey }} identifying the desired {{ model.className }}.
    
    @return: An empty flask reponse with status 404 if the desired {{ model.className }} cannot be found. An empty flask response with the status 204 if the desired {{ model.primaryKey }} has no {{ relationship.name }}. A flask response with the JSON list of the {{ relationship.name }} of the desired {{ model.className }}.
    """
    
    {{ model.className|lower }} = {{ model.className }}.{{ model.className }}.modelFor{{ model.primaryKey }}({{ model.primaryKey }})
    if not {{ model.className|lower }}:
        return flask.Response(
            resposne ='',
            status = 404,
            content_type = 'application/json'
        )
        
    {{ relationship.name }} = {{ relationship.type }}.{{ relationship.type }}.all({{ model.className|lower }} = {{ model.className|lower }}.{{ relationship.name }})
    
    if not {{ relationship.name }}:
        return flask.Response(
            response = '',
            status = 204,
            content_type = 'application/json'
        )
        
    {{ relationship.type|lower }}Dictionaries = [dict({{ relationship.type|lower }}) for {{ relationship.type|lower }} in {{ relationship.name }}]
    
    return flask.Response(
        response = json.dumps({{ relationship.type|lower }}Dictionaries),
        status = 200,
        content_type = 'application/json'
    )
    
def post{{ model.className|capitalize }}{{ relationship.name|capitalize }}({{ model.primaryKey }}, {{ relationship.name }}{{ model.primaryKey|capitalize }}):
    """
    Adds the given {{ relationship.name }}{{ model.primaryKey|capitalize }} to the desired {{ model.className }}'s {{ relationship.name }}.
    
    @param {{ model.primaryKey }}: The {{ model.primaryKey }} identifying the desired {{ model.className }}.
    @param {{ relationship.name }}{{ model.primaryKey|capitalize }}: The {{ model.primaryKey }} to add to the desired {{ model.className }}'s {{ relationship.name }}.
    
    @return: An empty flask reponse with status 404 if the desired {{ model.className }} cannot be found. An empty flask response with status 200 otherwise.
    """
    
    {{ model.className|lower }} = {{ model.className }}.{{ model.className }}.modelFor{{ model.primaryKey }}({{ model.primaryKey }})
    if not {{ model.className|lower }}:
        return flask.Response(
            resposne ='',
            status = 404,
            content_type = 'application/json'
        )
        
    {{ model.className|lower }}.{{ relationship.name }}.append({{ relationship.name }}{{ model.primaryKey|capitalize }})
    {{ model.className|lower }}.save()
    
    return flask.Response(
        response = '',
        status = 200,
        content_type = 'application/json'
    )
    
def delete{{ model.className|capitalize }}{{ relationship.name|capitalize }}({{ model.primaryKey }}, {{ relationship.name }}{{ model.primaryKey|capitalize }}):
    """
    Removes the given {{ relationship.name }}{{ model.primaryKey|capitalize }} from the desired {{ model.className }}'s {{ relationship.name }}.
    
    @param {{ model.primaryKey }}: The {{ model.primaryKey }} identifying the desired {{ model.className }}.
    @param {{ relationship.name }}{{ model.primaryKey|capitalize }}: The {{ model.primaryKey }} to remove from the desired {{ model.className }}'s {{ relationship.name }}.
    
    @return: An empty flask reponse with status 404 if the desired {{ model.className }} cannot be found. An empty flask response with status 200 otherwise.
    """
    
    {{ model.className|lower }} = {{ model.className }}.{{ model.className }}.modelFor{{ model.primaryKey }}({{ model.primaryKey }})
    if not {{ model.className|lower }}:
        return flask.Response(
            resposne ='',
            status = 404,
            content_type = 'application/json'
        )
        
    {{ model.className|lower }}.{{ relationship.name }}.remove({{ relationship.name }}{{ model.primaryKey|capitalize }})
    {{ model.className|lower }}.save()
    
    return flask.Response(
        response = '',
        status = 200,
        content_type = 'application/json'
    )
    
{%- else -%}
def get{{ model.className|capitalize }}{{ relationship.name|catpialize }}({{ model.primaryKey }}):
    """
    Returns the {{ relationship.name }} of the {{ model.className }} with the given {{ model.primaryKey }}.
    
    @param {{ model.primaryKey }}: The {{ model.primaryKey }} identifying the desired {{ model.className }}.
    
    @return: An empty flask reponse with status 404 if the desired {{ model.className }} cannot be found. A flask response with the JSON representation of the {{ relationship.name }} of the desired {{ model.className }}.
    """
    
    {{ model.className|lower }} = {{ model.className }}.{{ model.className }}.modelFor{{ model.primaryKey }}({{ model.primaryKey }})
    if not {{ model.className|lower }}:
        return flask.Response(
            resposne ='',
            status = 404,
            content_type = 'application/json'
        )
        
    {{ relationship.name }}s = {{ relationship.type }}.{{ relationship.type }}.all({{ model.primaryKey }} = {{ model.className|lower }}.{{ relationship.name }})
    
    if not {{ relationship.name }}s:
        return flask.Response(
            response = '',
            status = 204,
            content_type = 'application/json'
        )
        
    {{ relationship.name }}Dictionary = dict({{ relationship.name }}s[0])
    
    return flask.Response(
        response = json.dumps({{ relationship.name }}Dictionary),
        status = 200,
        content_type = 'application/json'
    )

def post{{ model.className|capitalize }}{{ relationship.name|catpialize }}({{ model.primaryKey }}, {{ relationship.name }}{{ model.primaryKey|capitalize }}):
    """
    Sets the {{ relationship.name }} of the {{ model.className }} with the given {{ model.primaryKey }} to the given value.
    
    @param {{ model.primaryKey }}: The {{ model.primaryKey }} identifying the desired {{ model.className }}.
    @param {{ relationship.name }}{{ model.primaryKey|capitalize }}: The {{ model.primaryKey }} of the {{ relationship.name }} to set as the {{ model.className }}'s {{ relationship.name }}.
    
    @return: An empty flask reponse with status 404 if the desired {{ model.className }} cannot be found. An empty flask response with status 200 otherwise.
    """
    
    {{ model.className|lower }} = {{ model.className }}.{{ model.className }}.modelFor{{ model.primaryKey }}({{ model.primaryKey }})
    if not {{ model.className|lower }}:
        return flask.Response(
            resposne ='',
            status = 404,
            content_type = 'application/json'
        )
        
    {{ model.className|lower }}.{{ relationship.name }} = {{ relationship.name }}{{ model.primaryKey|capitalize }}
    {{ model.className|lower }}.save()
    
    return flask.Response(
        response = '',
        status = 200,
        content_type = 'application/json'
    )
{% endfor -%}
{% endfor %}