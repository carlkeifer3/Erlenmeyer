#
#  ELUserHandler.py
#  ellog
#
#  Created by pcperini on Aug 28, 2013 via Erlenmeyer.
#  Copyright (c) 2013 pcperini. All rights reserved.
#

# imports
import json
import flask
from models import ELUser
from models import ELMessage


# handlers
def getELUsers(**kwargs):
    """
    Returns a list of all ELUsers.
        
    @return: A flask response built with a JSON list of all ELUsers.
    """
    
    for key in kwargs:
        if type(kwargs[key]) == list:
            kwargs[key] = kwargs[key][0]
    
    allELUsers = ELUser.ELUser.all(**kwargs)
    allELUsersDictionaries = [dict(eluser) for eluser in allELUsers if dict(eluser)]
    
    return flask.Response(
        response = json.dumps(allELUsersDictionaries),
        status = 200,
        content_type = 'application/json'
    )
    
def putELUser(properties):
    """
    Inserts a new ELUser with the given properties into the database.
        
    @param properties: A series of key-value pairs to apply to the new ELUser.
    
    @return: An empty flask response.
    """
    
    uuid = properties['uuid']
    if type(uuid) == list:
        uuid = uuid[0]
    
    eluser = ELUser.ELUser.get(uuid)
    if not eluser:
        eluser = ELUser.ELUser()
    
    eluser.update(properties)    
    eluser.save()
    
    return flask.Response(
        response = '',
        status = 200,
        content_type = 'application/json'
    )
    
def getELUser(uuid):
    """
    Returns the ELUser with the given uuid.
        
    @param uuid: The uuid identifying the desired ELUser.
    
    @return: An empty flask response with status 404 if the desired ELUser cannot be found. A flask response built with the JSON dictionary for the desired ELUser otherwise.
    """
    
    eluser = ELUser.ELUser.get(uuid)
    if not eluser:
        return flask.Response(
            response = '',
            status = 404,
            content_type = 'application/json'
        )
        
    eluserDictionary = dict(eluser)
    
    return flask.Response(
        response = json.dumps(eluserDictionary),
        status = 200,
        content_type = 'application/json'
    )
    
def postELUser(uuid, properties):
    """
    Updates the ELUser with the given uuid to have the given properties.
        
    @param uuid: The uuid identifying the desired ELUser.
    @param properties: A series of key-value pairs to apply to the desired ELUser.
    
    @return: An empty flask response with status 404 if the desired ELUser cannot be found. An empty flask response with status 200 otherwise.
    """
    
    eluser = ELUser.ELUser.get(uuid)
    if not eluser:
        return flask.Response(
            response = '',
            status = 404,
            content_type = 'application/json'
        )
        
    eluser.update(properties)        
    eluser.save()
    
    return flask.Response(
        response = '',
        status = 200,
        content_type = 'application/json'
    )
    
def deleteELUser(uuid):
    """
    Deletes the ELUser with the given uuid.
        
    @param : The uuid identifying the desired ELUser.
    
    @return: An empty flask reponse with status 404 if the desired ELUser cannot be found. An empty flask response with status 200 otherwise.
    """
    
    eluser = ELUser.ELUser.get(uuid)
    if not eluser:
        return flask.Response(
            response = '',
            status = 404,
            content_type = 'application/json'
        )
        
    eluser.delete()
    
    return flask.Response(
        response = '',
        status = 200,
        content_type = 'application/json'
    )
    
# - relationships
def getELUserMessages(uuid):
    """
    Returns the messages of the ELUser with the given uuid.
    
    @param uuid: The uuid identifying the desired ELUser.
    
    @return: An empty flask reponse with status 404 if the desired ELUser cannot be found. A flask response with the JSON list of the messages of the desired ELUser.
    """
    
    eluser = ELUser.ELUser.get(uuid)
    if not eluser:
        return flask.Response(
            response = '',
            status = 404,
            content_type = 'application/json'
        )
        
    messagesDictionaries = []
    for elmessage in eluser.messages:
        elmessageDictionary = dict(elmessage)
        
        messagesDictionaries.append(elmessageDictionary)
        
    return flask.Response(
        response = json.dumps(messagesDictionaries),
        status = 200,
        content_type = 'application/json'
    )
    
def putELUserMessages(uuid, messagesUuid):
    """
    Adds the given messagesUuid to the desired ELUser's messages.
        
    @param uuid: The uuid identifying the desired ELUser.
    @param messagesUuid: The uuid to add to the desired ELUser's messages.
    
    @return: An empty flask reponse with status 404 if the desired ELUser cannot be found. An empty flask response with status 200 otherwise.
    """
    
    eluser = ELUser.ELUser.get(uuid)
    if not eluser:
        return flask.Response(
            response = '',
            status = 404,
            content_type = 'application/json'
        )
    
    elmessage = ELMessage.ELMessage.get(messagesUuid)
    if not elmessage:
        return flask.Response(
            response = '',
            status = 400,
            content_type = 'application/json'
        )
    
    if elmessage not in eluser.messages:
        eluser.messages.append(elmessage)
    
    eluser.save()
        
    return flask.Response(
        response = '',
        status = 200,
        content_type = 'application/json'
    )
    
def deleteELUserMessages(uuid, messagesUuid):
    """
    Removes the given messagesUuid from the desired ELUser's messages.
        
    @param uuid: The uuid identifying the desired ELUser.
    @param messagesUuid: The uuid to remove from the desired ELUser's messages.
    
    @return: An empty flask reponse with status 404 if the desired ELUser cannot be found. An empty flask response with status 200 otherwise.
    """
    
    eluser = ELUser.ELUser.get(uuid)
    if not eluser:
        return flask.Response(
            response = '',
            status = 404,
            content_type = 'application/json'
        )
    
    elmessage = ELMessage.ELMessage.get(messagesUuid)
    if not elmessage:
        return flask.Response(
            response = '',
            status = 400,
            content_type = 'application/json'
        )
    
    if elmessage in eluser.messages:
        eluser.messages.remove(elmessage)
    
    eluser.save()
        
    return flask.Response(
        response = '',
        status = 200,
        content_type = 'application/json'
    )
    
