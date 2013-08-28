#
#  ELMessageHandler.py
#  ellog
#
#  Created by pcperini on Aug 28, 2013 via Erlenmeyer.
#  Copyright (c) 2013 pcperini. All rights reserved.
#

# imports
import json
import flask
from models import ELMessage
from models import ELUser


# handlers
def getELMessages(**kwargs):
    """
    Returns a list of all ELMessages.
        
    @return: A flask response built with a JSON list of all ELMessages.
    """
    
    for key in kwargs:
        if type(kwargs[key]) == list:
            kwargs[key] = kwargs[key][0]
    
    allELMessages = ELMessage.ELMessage.all(**kwargs)
    allELMessagesDictionaries = [dict(elmessage) for elmessage in allELMessages if dict(elmessage)]
    
    return flask.Response(
        response = json.dumps(allELMessagesDictionaries),
        status = 200,
        content_type = 'application/json'
    )
    
def putELMessage(properties):
    """
    Inserts a new ELMessage with the given properties into the database.
        
    @param properties: A series of key-value pairs to apply to the new ELMessage.
    
    @return: An empty flask response.
    """
    
    uuid = properties['uuid']
    if type(uuid) == list:
        uuid = uuid[0]
    
    elmessage = ELMessage.ELMessage.get(uuid)
    if not elmessage:
        elmessage = ELMessage.ELMessage()
    
    elmessage.update(properties)    
    elmessage.save()
    
    return flask.Response(
        response = '',
        status = 200,
        content_type = 'application/json'
    )
    
def getELMessage(uuid):
    """
    Returns the ELMessage with the given uuid.
        
    @param uuid: The uuid identifying the desired ELMessage.
    
    @return: An empty flask response with status 404 if the desired ELMessage cannot be found. A flask response built with the JSON dictionary for the desired ELMessage otherwise.
    """
    
    elmessage = ELMessage.ELMessage.get(uuid)
    if not elmessage:
        return flask.Response(
            response = '',
            status = 404,
            content_type = 'application/json'
        )
        
    elmessageDictionary = dict(elmessage)
    
    return flask.Response(
        response = json.dumps(elmessageDictionary),
        status = 200,
        content_type = 'application/json'
    )
    
def postELMessage(uuid, properties):
    """
    Updates the ELMessage with the given uuid to have the given properties.
        
    @param uuid: The uuid identifying the desired ELMessage.
    @param properties: A series of key-value pairs to apply to the desired ELMessage.
    
    @return: An empty flask response with status 404 if the desired ELMessage cannot be found. An empty flask response with status 200 otherwise.
    """
    
    elmessage = ELMessage.ELMessage.get(uuid)
    if not elmessage:
        return flask.Response(
            response = '',
            status = 404,
            content_type = 'application/json'
        )
        
    elmessage.update(properties)        
    elmessage.save()
    
    return flask.Response(
        response = '',
        status = 200,
        content_type = 'application/json'
    )
    
def deleteELMessage(uuid):
    """
    Deletes the ELMessage with the given uuid.
        
    @param : The uuid identifying the desired ELMessage.
    
    @return: An empty flask reponse with status 404 if the desired ELMessage cannot be found. An empty flask response with status 200 otherwise.
    """
    
    elmessage = ELMessage.ELMessage.get(uuid)
    if not elmessage:
        return flask.Response(
            response = '',
            status = 404,
            content_type = 'application/json'
        )
        
    elmessage.delete()
    
    return flask.Response(
        response = '',
        status = 200,
        content_type = 'application/json'
    )
    
# - relationships
def getELMessageAuthor(uuid):
    """
    Returns the author of the ELMessage with the given uuid.
        
    @param uuid: The uuid identifying the desired ELMessage.
    
    @return: An empty flask reponse with status 404 if the desired ELMessage cannot be found. A flask response with the JSON representation of the author of the desired ELMessage.
    """
    
    elmessage = ELMessage.ELMessage.get(uuid)
    if not elmessage:
        return flask.Response(
            response = '',
            status = 404,
            content_type = 'application/json'
        )
        
    if not elmessage.author:
        return flask.Response(
            response = json.dumps({}),
            status = 200,
            content_type = 'application/json'
        )
        
    eluser = ELUser.ELUser.get(elmessage.author)
    authorDictionary = dict(eluser)
        
    return flask.Response(
        response = json.dumps(authorDictionary),
        status = 200,
        content_type = 'application/json'
    )
    
def postELMessageAuthor(uuid, authorUuid):
    """
    Sets the author of the ELMessage with the given uuid to the given value.
        
    @param uuid: The uuid identifying the desired ELMessage.
    @param authorUuid: The uuid of the author to set as the ELMessage's author.
    
    @return: An empty flask reponse with status 404 if the desired ELMessage cannot be found. An empty flask response with status 200 otherwise.
    """
    
    elmessage = ELMessage.ELMessage.get(uuid)
    if not elmessage:
        return flask.Response(
            response = '',
            status = 404,
            content_type = 'application/json'
        )
        
    eluser = ELUser.ELUser.get(authorUuid)
    if not eluser:
        return flask.Response(
            response = '',
            status = 400,
            content_type = 'application/json'
        )
        
    elmessage.author = eluser.uuid
    elmessage.save()
        
    return flask.Response(
        response = '',
        status = 200,
        content_type = 'application/json'
    )
    
