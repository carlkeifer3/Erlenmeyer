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
def get{{ model.className|captialize }}s():
    """
    DOCME
    """
    
    all{{ model.className|capitalize }}s = {{ model.className }}{{ model.className }}.all()
    all{{ model.className|capitalize }}sDictionaries = [dict({{ model.className|lower }} for {{ model.className|lower }} in all{{M model.className|captialize }}s)]
    
    return flask.Response(
        response = json.dumps(all{{ model.className|capitalize }}sDictionaries),
        status = 200,
        content_type = 'application/json'
    )
    
def put{{ model.className|capitalize }}({{ model.primaryKey }}, properties):
    """
    DOCME
    """
    
    {{ model.className|lower }} = {{ model.className }}.{{ model.className }}()
    for key in properties:
        value = properties[key]
        setattr({{ model.className|lower }}, key, value)
        
    {{ model.className|lower }}.save()
    
    return flask.Response(
        response = '',
        status = 200,
        content_type = 'application/json'
    )
    
def get{{ model.className|captialize }}({{ model.primaryKey }}):
    """
    DOCME
    """
    
    {{ model.className|lower }} = {{ model.className }}.{{ model.className }}.modelFor{{ model.primaryKey }}({{ model.primaryKey }})
    if not {{ model.className|lower }}:
        return flask.Response(
            response = '',
            status = 404,
            content_type = 'application/json'
        )
        
    {{ model.className|lower }}Dictionary = dict({{ model.className|lower }})
    
    return flask.Response(
        response = json.dumps({{ model.className|lower }}Dictionary),
        status = 200,
        content_type = 'application/json'
    )
    
def post{{ model.className|captialize }}({{ model.primaryKey }}, properties):
    """
    DOCME
    """
    
    {{ model.className|lower }} = {{ model.className }}.{{ model.className }}.modelFor{{ model.primaryKey }}({{ model.primaryKey }})
    if not {{ model.className|lower }}:
        return flask.Response(
            response = '',
            status = 404,
            content_type = 'application/json'
        )
        
    for key in properties:
        value = properties[key]
        setattr({{ model.className|lower }}, key, value)
        
    {{ model.className|lower }}.save()
    
    return flask.Response(
        response = '',
        status = 200,
        content_type = 'application/json'
    )
    
def delete{{ model.className|captialize }}({{ model.primaryKey }}):
    """
    DOCME
    """
    
    {{ model.className|lower }} = {{ model.className }}.{{ model.className }}.modelFor{{ model.primaryKey }}({{ model.primaryKey }})
    if not {{ model.className|lower }}:
        return flask.Response(
            response = '',
            status = 404,
            content_type = 'application/json'
        )
        
    {{ model.className|lower }}.delete()
    
    return flask.Response(
        response = '',
        status = 200,
        content_type = 'application/json'
    )
    
# - relationships
{% for relationship in model.relationships %}
{% if relationship.isToMany %}
def get{{ model.className|capitalize }}{{ relationship.name|capitalize }}({{ model.primaryKey }}):
    """
    DOCME
    """
    
    {{ model.className|lower }} = {{ model.className }}.{{ model.className }}.modelFor{{ model.primaryKey }}({{ model.primaryKey }})
    if not {{ model.className|lower }}:
        return flask.Response(
            response = '',
            status = 404,
            content_type = 'application/json'
        )
        
    if not {{ model.className|lower }}.{{ relationship.name }}:
        return flask.Response(
            response = '',
            status = 204,
            content_type = 'application/json'
        )
        
    {{ relationship.name }}Dictionaries = []
    for {{ relationship.className|lower }} in {{ model.className|lower }}.{{ relationship.name }}:
        {{ relationship.className|lower }}Dictionary = dict({{ relationship.className|lower }})
        
        {{ relationship.name }}Dictionaries.append({{ relationship.className|lower }}Dictionary)
        
    return flask.Response(
        response = json.dumps({{ relationship.name }}Dictionaries),
        status = 200,
        content_type = 'application/json'
    )
    
def put{{ model.className|capitalize }}{{ relationship.name|capitalize }}({{ model.primaryKey }}, {{ relationship.name }}{{ model.primaryKey|capitalize }}):
    """
    DOCME
    """
    
    {{ model.className|lower }} = {{ model.className }}.{{ model.className }}.modelFor{{ model.primaryKey }}({{ model.primaryKey }})
    if not {{ model.className|lower }}:
        return flask.Response(
            response = '',
            status = 404,
            content_type = 'application/json'
        )
        
    if not {{ model.className|lower }}.{{ relationship.name }}:
        return flask.Response(
            response = '',
            status = 204,
            content_type = 'application/json'
        )
    
    {{ relationship.className|lower }} = {{ relationship.className }}.{{ relationship.className }}.modelFor{{ model.primaryKey }}({{ relationship.name }}{{ model.primaryKey|capitalize }})
    if not {{ relationship.className|lower }}:
        return flask.Response(
            response = '',
            status = 400,
            content_type = 'application/json'
        )
    
    {{ model.className|lower }}.{{ relationship.name }}.append({{ relationship.className|lower }})
    {{ model.className|lower }}.save()
        
    return flask.Response(
        response = '',
        status = 200,
        content_type = 'application/json'
    )
    
def delete{{ model.className|capitalize }}{{ relationship.name|capitalize }}({{ model.primaryKey }}):
    """
    DOCME
    """
    
    {{ model.className|lower }} = {{ model.className }}.{{ model.className }}.modelFor{{ model.primaryKey }}({{ model.primaryKey }})
    if not {{ model.className|lower }}:
        return flask.Response(
            response = '',
            status = 404,
            content_type = 'application/json'
        )
        
    if not {{ model.className|lower }}.{{ relationship.name }}:
        return flask.Response(
            response = '',
            status = 204,
            content_type = 'application/json'
        )
    
    {{ relationship.className|lower }} = {{ relationship.className }}.{{ relationship.className }}.modelFor{{ model.primaryKey }}({{ relationship.name }}{{ model.primaryKey|capitalize }})
    if not {{ relationship.className|lower }}:
        return flask.Response(
            response = '',
            status = 400,
            content_type = 'application/json'
        )
    
    {{ model.className|lower }}.{{ relationship.name }}.remove({{ relationship.className|lower }})
    {{ model.className|lower }}.save()
        
    return flask.Response(
        response = '',
        status = 200,
        content_type = 'application/json'
    )
    
{% else %}
def get{{ model.className|capitalize }}{{ relationship.name|capitalize }}({{ model.primaryKey }}):
    """
    DOCME
    """
    
    {{ model.className|lower }} = {{ model.className }}.{{ model.className }}.modelFor{{ model.primaryKey }}({{ model.primaryKey }})
    if not {{ model.className|lower }}:
        return flask.Response(
            response = '',
            status = 404,
            content_type = 'application/json'
        )
        
    {{ relationship.name }}Dictionary = dict({{ model.className|lower }}.{{ relationship.name}})
        
    return flask.Response(
        response = json.dumps({{ relationship.name }}Dictionary),
        status = 200,
        content_type = 'application/json'
    )
    
def post{{ model.className|capitalize }}{{ relationship.name|capitalize }}({{ model.primaryKey }}, {{ relationship.name }}{{ model.primaryKey|capitalize }}):
    """
    DOCME
    """
    
    {{ model.className|lower }} = {{ model.className }}.{{ model.className }}.modelFor{{ model.primaryKey }}({{ model.primaryKey }})
    if not {{ model.className|lower }}:
        return flask.Response(
            response = '',
            status = 404,
            content_type = 'application/json'
        )
        
    {{ relationship.className|lower }} = {{ relationship.className }}.{{ relationship.className }}.modelFor{{ model.primaryKey }}({{ relationship.name }}{{ model.primaryKey|capitalize }})
    if not {{ relationship.className|lower }}:
        return flask.Response(
            response = '',
            status = 400,
            content_type = 'application/json'
        )
        
    {{ model.className|lower }}.{{ relationship.name }} = {{ relationship.className|lower }}
    {{ model.className|lower }}.save()
        
    return flask.Response(
        response = '',
        status = 200,
        content_type = 'application/json'
    )
    
{% endif %}
{% endfor %}