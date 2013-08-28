#
#  ELMessage.py
#  ellog
#
#  Created by pcperini on Aug 28, 2013 via Erlenmeyer.
#  Copyright (c) 2013 pcperini. All rights reserved.
#

# imports
from ellog import database

class ELMessage (database.Model):

    # class properties
    __database__ = database

    # properties
    text = database.Column(database.String(256))
    timestamp = database.Column(database.Integer)
    uuid = database.Column(database.String(256), primary_key = True)
    
    
    # - relationships
    _author_uuid = database.Column(database.String(256), database.ForeignKey("el_user.uuid"))
    author = database.relationship("ELUser", backref = database.backref("messages"))
    
    