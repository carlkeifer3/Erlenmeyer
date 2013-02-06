#
#  {{ metadata.fileName }}
#  {{ metadata.projectName }}
#
#  Created by {{ metadata.fileAuthor }} on {{ metadata.pubDate }} via Erlenmeyer.
#  Copyright (c) {{ metadata.pubYear }} {{ metadata.projectOwner }}. All rights reserved.
#

# imports
from flask.ext.sqlalchemy import SQLAlchemy

# globals
database = None

class Model (database.Model):
    """
    DOCME
    """
    
    # properties
    {{ model.primaryKey }} = database.Column(database.String(256), primary_key = True)
    
    # class accessors
    @classmethod
    def modelFor{{ model.primaryKey }}(self, {{ model.primaryKey }}):
        """
        DOCME
        """
        
        return User.query.get({{ model.primaryKey }})
        
    # accessors
    def __iter__(self):
        for key in self.__dict__:
            if key.startswith('_'):
              continue
              
            yield (key, self.__dict__[key])  
    
    # mutators
    def save(self):
        """
        DOCME
        """
        
        database.session.add(self)
        database.session.commit()
        
    def delete(self):
        """
        DOCME
        """
        
        database.session.delete(self)
        database.session.commit()