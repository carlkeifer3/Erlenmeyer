#
#  Model_extensions.py
#  Erlenmeyer
#
#  Created by Patrick Perini on February 7, 2013.
#  See LICENSE.txt for licensing information.
#

# imports
from flask.ext.sqlalchemy import SQLAlchemy

# accessors
def __iter__(self):
    for key in self.__dict__:
        if not key.startswith('_'):
            yield (key, self.__dict__[key])  

# mutators
def update(self, properties):
    for key in properties:
        setattr(self, key, properties[key])

def save(self):
    database.session.add(self)
    database.session.commit()
    
def delete(self):
    database.session.delete(self)
    database.session.commit()