#
#  {{ metadata.fileName }}
#  {{ metadata.projectName }}
#
#  Created by {{ metadata.fileAuthor }} on {{ metadata.pubDate }} via Erlenmeyer.
#  Copyright (c) {{ metadata.pubYear }} {{ metadata.projectOwner }}. All rights reserved.
#

# imports
from erlenmeyer import Model
import {{ model.parentClassName }}

class {{ model.className }} ({{ model.parentClassName }}):

    # properties
    {% for attribute in model.attributes -%}
    {% if {{ attribute.name }} == {{ model.primaryKey }} -%}
    {{ attribute.name }} = Model.database.Column(Model.database.{{ attribute.type }}, primary_key = True)
    {% else -%}
    {{ attribute.name }} = Model.database.Column(Model.database.{{ attribute.type }})
    {% endif -%}
    {% else %}
    # - no attributes...
    {% endfor %}
    
    # - relationships
    {% for relationship in model.relationships -%}
    {% if relationship.isToMany -%}
    {{ relationship.name }} = Model.database.relationship(
        '{{ relationship.className }}',
        Model.database.ForeignKey('{{ relationship.className }}.{{ model.primaryKey }}')
    )
    {% else -%}
    {{ relationship.name }} = Model.database.relationship(
        '{{ relationship.className }}',
        Model.database.ForeignKey('{{ relationship.className }}.{{ model.primaryKey }}'),
        uselist = False
    )
    {% endif -%}
    {% else %}
    # - no relationships...
    {% endfor %}