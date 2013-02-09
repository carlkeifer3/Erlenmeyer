#
#  {{ metadata.fileName }}
#  {{ metadata.projectName }}
#
#  Created by {{ metadata.fileAuthor }} on {{ metadata.pubDate }} via Erlenmeyer.
#  Copyright (c) {{ metadata.pubYear }} {{ metadata.projectOwner }}. All rights reserved.
#

# imports
from {{ metadata.projectName }} import database
{% if model.parentClassName != "database.Model" -%}
from {{ model.parentClassName }} import {{ model.parentClassName }}
{%- endif %}

class {{ model.className }} ({{ model.parentClassName }}):

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
    {{ relationship.name }} = database.relationship(
        '{{ relationship.className }}',
        database.ForeignKey('{{ relationship.className }}.{{ model.primaryKey }}')
    )
    {% else -%}
    {{ relationship.name }} = database.relationship(
        '{{ relationship.className }}',
        database.ForeignKey('{{ relationship.className }}.{{ model.primaryKey }}'),
        uselist = False
    )
    {% endif -%}
    {% else %}
    # - - no relationships...
    {% endfor %}