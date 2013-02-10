#
#  {{ metadata.fileName }}
#  {{ metadata.projectName }}
#
#  Created by {{ metadata.fileAuthor }} on {{ metadata.pubDate }} via Erlenmeyer.
#  Copyright (c) {{ metadata.pubYear }} {{ metadata.projectOwner }}. All rights reserved.
#

# imports
from erlenmeyer.libs import jinja2_filters
from {{ metadata.projectName }} import database

class {{ model.className }} (database.Model):

    # class properties
    __database__ = database

    # properties
    {% for attribute in model.attributes -%}
    {% if attribute.name == model.primaryKey -%}
    {{ attribute.name }} = database.Column(database.{{ attribute.type }}, primary_key = True)
    {% else -%}
    {{ attribute.name }} = database.Column(database.{{ attribute.type }})
    {% endif -%}
    {% else %}
    # - no properties...
    {% endfor %}
    
    # - relationships
    {% for relationship in model.relationships -%}
    {% if relationship.isToMany -%}
    {{ relationship.name }} = database.relationship('{{ relationship.className }}')
    {% else -%}
    {{ relationship.name }} = database.Column(database.{{ model.primaryKeyType }}, database.ForeignKey('{{ relationship.className|underscore }}.{{ model.primaryKey }}'))
    {% endif -%}
    {% else %}
    # - - no relationships...
    {% endfor %}