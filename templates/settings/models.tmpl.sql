#
#  SQL Setup
#  {{ metadata.projectName }}
#
#  Created by {{ metadata.fileAuthor }} on {{ metadata.pubDate }} via Erlenmeyer.
#  Copyright (c) {{ metadata.pubYear }} {{ metadata.projectOwner }}. All rights reserved.
#

{% for model in models -%}
DROP TABLE IF EXISTS `{{ model.className|lower }}s`;
CREATE TABLE `{{ model.className|lower }}s` (
    # attributes
    {% for attribute in model.attributes -%}
    `{{ attribute.name }}` {{ attribute.sqlType }}{{ " NOT NULL" if not attribute.canBeNull }},
    {% endfor %}
    
    # relationships
    {% for relationship in model.relationships -%}
    {% if not relationship.toMany -%}
    `{{ relationship.name }}` {{ relationship.sqlType }}{{ " NOT NULL" if not relationship.canBeNull }},
    {% endif -%}
    {% endfor %}
    
    PRIMARY KEY (`{{ model.primaryKey }}`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

{% for relationship in model.relationships -%}
{% if relationship.toMany -%}
DROP TABLE IF EXISTS `{{ model.className|lower }}s{{ relationship.capsName }}`;
CREATE TABLE `{{ model.className|lower }}s{{ relationship.capsName }}` (
    `{{ model.className|lower }}s` {{ relationship.sqlType }} NOT NULL,
    `{{ relationship.name }}` {{ relationship.sqlType }} NOT NULL,
    
    PRIMARY KEY (`{{ model.className }}`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
{% endif -%}
{% endfor -%}
{% endfor -%}