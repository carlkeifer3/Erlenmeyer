#
#  ELUser.py
#  ellog
#
#  Created by pcperini on Aug 28, 2013 via Erlenmeyer.
#  Copyright (c) 2013 pcperini. All rights reserved.
#

# imports
from ellog import database

class ELUser (database.Model):

    # class properties
    __database__ = database

    # properties
    username = database.Column(database.String(256))
    uuid = database.Column(database.String(256), primary_key = True)
    
    
    # - relationships
    
    