#
#  CoreData.py
#  Erlenmeyer
#
#  Created by Patrick Perini on February 6, 2013.
#  See LICENSE.txt for licensing information.
#

# imports
import os
from xml.dom import minidom
    

class CoreData (dict):
    """
    A dictionary parsed from an .xcodedatamodeld file.
    """
    
    # initializes
    def __init__(self, coreDataFile, primaryKey = 'uuid'):
        """
        Creates a CoreData dictionary object from the given .xcodedatamodeld file.
        
        @param coreDataFile: The path to the .xcodedatamodeld file for parsing.
        @param primaryKey: The primaryKey for the Model class. All other models will inherit this key. Defaults to 'uuid'.
        
        @returns: A CoreData dictionary object.
        """
        
        coreDataFile = '%s/%s/contents' % (coreDataFile, os.path.basename(coreDataFile[:-1]))
        self.__parseCoreDataFile(coreDataFile, primaryKey)
        
    # accessors
    def __entityForDOMEntity(self, domEntity, primaryKey):
        entity = {
            "className": str(domEntity.getAttributeNode('name').nodeValue),
            "parentClassName": "database.Model",
            "primaryKey": primaryKey,
            "attributes": [],
            "relationships": []
        }
        
        if domEntity.getAttributeNode('parentEntity'):
            entity['parentClassName'] = str(domEntity.getAttributeNode('parentEntity').nodeValue)
        
        domAttributes = domEntity.getElementsByTagName('attribute')
        for domAttribute in domAttributes:
            entity['attributes'].append(self.__attributeForDOMAttribute(domAttribute))
            
        domRelationships = domEntity.getElementsByTagName('relationship')
        for domRelationship in domRelationships:
            entity['relationships'].append(self.__relationshipForDOMRelationship(domRelationship))
            
        return entity
            
    def __attributeForDOMAttribute(self, domAttribute):
        attribute = {
            "name": str(domAttribute.getAttributeNode('name').nodeValue),
            "type": "String(256)",
        }
        
        if domAttribute.getAttributeNode('attributeType'):
            attributeType = str(domAttribute.getAttributeNode('attributeType').nodeValue)
            
            if "Integer" in attributeType:
                attribute['type'] = "Integer"
            elif attributeType in ["Decimal", "Double", "Float"]:
                attribute['type'] = "Float"
            elif "Boolean" in attributeType:
                attribute['type'] = "Boolean"
                
        return attribute
        
    def __relationshipForDOMRelationship(self, domRelationship):
        relationship = {
            "name": str(domRelationship.getAttributeNode('name').nodeValue),
            "className": str(domRelationship.getAttributeNode('destinationEntity').nodeValue),
            "isToMany": False
        }
        
        if domRelationship.getAttributeNode('toMany'):
            relationship['isToMany'] = str(domRelationship.getAttributeNode('toMany').nodeValue) == 'YES'
            
        return relationship
        
    # mutators
    def __parseCoreDataFile(self, coreDataFile, primaryKey):
        coreDataFile = open(coreDataFile)
        coreDataDOM = minidom.parse(coreDataFile)
        
        self['models'] = []
        domEntities = coreDataDOM.getElementsByTagName('entity')
        for domEntity in domEntities:
            self['models'].append(self.__entityForDOMEntity(domEntity, primaryKey))