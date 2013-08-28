#
#  ellog.py
#  ellog
#
#  Created by pcperini on Aug 28, 2013 via Erlenmeyer.
#  Copyright (c) 2013 pcperini. All rights reserved.
#

# imports
import os
import json
import flask
from erlenmeyer import categories
from flask.ext.sqlalchemy import SQLAlchemy
from erlenmeyer.ext import Model as ModelExtensions
from erlenmeyer.ext import SQLAlchemy as SQLAlchemyExtensions

# globals
__filepath__ = os.path.dirname(os.path.abspath(__file__))
settings = json.load(open('%s/settings/settings.json' % (__filepath__)))

flaskApp = flask.Flask(__name__)
flaskApp.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://bqqlizmsljbumy:v9b6fprC4gBl2-SglJJ0GQ8LWr@ec2-54-225-112-205.compute-1.amazonaws.com:5432/d7nm91r166vsdj"# os.environ['DATABASE_URL']

database = SQLAlchemy(flaskApp)
categories.addCategories(database, SQLAlchemyExtensions, list = SQLAlchemyExtensions.instanceMethods)
categories.addCategories(database.Model.__class__, ModelExtensions, list = ModelExtensions.classMethods)
categories.addCategories(database.Model, ModelExtensions, list = ModelExtensions.instanceMethods)



# handlers
# - ELMessage
@flaskApp.route("/ELMessages", methods = ["GET", "PUT"])
def handleELMessages():
    from handlers import ELMessageHandler
    
    
    
    if flask.request.method == "GET":
        return ELMessageHandler.getELMessages(**dict(flask.request.args))
        
    elif flask.request.method == "PUT":
        return ELMessageHandler.putELMessage(dict(flask.request.form))
        
@flaskApp.route("/ELMessages/<uuid>", methods = ["GET", "POST", "DELETE"])
def handleELMessage(uuid):
    from handlers import ELMessageHandler
    
    

    if flask.request.method == "GET":
        return ELMessageHandler.getELMessage(uuid)
        
    elif flask.request.method == "POST":
        return ELMessageHandler.postELMessage(uuid, dict(flask.request.form))
        
    elif flask.request.method == "DELETE":
        return ELMessageHandler.deleteELMessage(uuid)
        
# - - author
@flaskApp.route("/ELMessages/<uuid>/author", methods = ["GET", "POST"])
def handleELMessageAuthor(uuid):
    from handlers import ELMessageHandler
    
    
    
    if flask.request.method == "GET":
        return ELMessageHandler.getELMessageAuthor(uuid)
        
    elif flask.request.method == "POST":
        return ELMessageHandler.postELMessageAuthor(uuid, flask.request.form['authorObject'])


# - ELUser
@flaskApp.route("/ELUsers", methods = ["GET", "PUT"])
def handleELUsers():
    from handlers import ELUserHandler
    
    
    
    if flask.request.method == "GET":
        return ELUserHandler.getELUsers(**dict(flask.request.args))
        
    elif flask.request.method == "PUT":
        return ELUserHandler.putELUser(dict(flask.request.form))
        
@flaskApp.route("/ELUsers/<uuid>", methods = ["GET", "POST", "DELETE"])
def handleELUser(uuid):
    from handlers import ELUserHandler
    
    

    if flask.request.method == "GET":
        return ELUserHandler.getELUser(uuid)
        
    elif flask.request.method == "POST":
        return ELUserHandler.postELUser(uuid, dict(flask.request.form))
        
    elif flask.request.method == "DELETE":
        return ELUserHandler.deleteELUser(uuid)
        
# - - messages
@flaskApp.route("/ELUsers/<uuid>/messages", methods = ["GET", "PUT", "DELETE"])
def handleELUserMessages(uuid):
    from handlers import ELUserHandler

    

    if flask.request.method == "GET":
        return ELUserHandler.getELUserMessages(uuid)
        
    elif flask.request.method == "PUT":
        return ELUserHandler.putELUserMessages(uuid, flask.request.form['messagesObject'])
        
    elif flask.request.method == "DELETE":
        return ELUserHandler.deleteELUserMessages(uuid, flask.request.args['messagesObject'])
        



# functions
def createTables():
    from ellog import database
    from models.ELMessage import ELMessage
    from models.ELUser import ELUser
    
    
    database.create_all()

# main
if __name__ == "__main__":    
    createTables()

    flaskApp.run(
        host = settings['server']['ip'],
        port = settings['server']['port'],
        debug = settings['server']['debug']
    )