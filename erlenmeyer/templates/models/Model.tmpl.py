#
#  {{ metadata.fileName }}
#  {{ metadata.projectName }}
#
#  Created by {{ metadata.fileAuthor }} on {{ metadata.pubDate }} via Erlenmeyer.
#  Copyright (c) {{ metadata.pubYear }} {{ metadata.projectOwner }}. All rights reserved.
#

# imports
from flask.ext.sqlalchemy import SQLAlchemy

# constants
{{ model.primaryKey }}Header = "{{ model.primaryKey|upper }}"

# globals
database = None

# functions
_{{ model.primaryKey }} = lambda: '%s%s' % ({{ model.primaryKey }}Header, str(uuid.uuid4()).replace('-', ''))

class Model (database.Model):
    """
    Baseclass for custom user models.
    """
    
    # properties
    {{ model.primaryKey }} = database.Column(database.String(256), primary_key = True)
    
    # class accessors
    @classmethod
    def modelFor{{ model.primaryKey|camelcase }}(self, {{ model.primaryKey }}):
        """
        Return an instance of the object based on the given identifier, or None if not found.
        
        @param {{ model.primaryKey }}: The identifier of the desired object.
        
        @returns: An instance of the object based no the given identifier, or None if not found.
        """
        
        return User.query.get({{ model.primaryKey }})
        
    # initializers
    def __init__(self):
        """
        Initializes a new object with a unique {{ model.primaryKey }}.
        """
        
        self.{{ model.primaryKey }} = _{{ model.primaryKey }}()
        
    # accessors
    def __iter__(self):
        for key in self.__dict__:
            if key.startswith('_'):
              continue
              
            yield (key, self.__dict__[key])  
    
    # mutators
    def save(self):
        """
        Saves this object to the database.
        """
        
        database.session.add(self)
        database.session.commit()
        
    def delete(self):
        """
        Deletes this object from the database.
        """
        
        database.session.delete(self)
        database.session.commit()