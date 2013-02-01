#
#  {{ metadata.fileName }}
#  {{ metadata.projectName }}
#
#  Created by {{ metadata.fileAuthor }} on {{ metadata.pubDate }}.
#  Copyright (c) {{ metadata.pubYear }} {{ metadata.projectOwner }}. All rights reserved.
#

# imports
import {{ model.parentName }}

class {{ model.className }} ({{ model.parentName }}.{{ model.parentName }}):
    # initializers
    def __init__(self, dictionary = None):
        super(self.__class__, self).__init__(dictionary)
        
        # attributes
        {% for attribute in model.attributes -%}
        self.__class__.{{ attribute.name }} = self.property("{{ attribute.name }}", {{ attribute.defaultValue }})
        {% endfor %}
        
        # relationships
        {% for relationship in model.relationships -%}
        self.__class__.{{ relationship.name }} = self.property("{{ relationship.name }}", {{ [] if relationship.toMany else None }})
        {% endfor %}