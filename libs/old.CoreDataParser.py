#
#  CoreDataParser.py
#  Erlenmeyer
#
#  Created by Patrick Perini on February 3, 2013.
#  See readme.md for licensing information.
#

#imports
import os
from xml.dom import minidom

#functions
def dictionary(coreDataFile, primaryKey = "uuid"):
    """
    DOCME
    """
    
    coreDataFile = '%s/%s/contents' % (coreDataFile, os.path.basename(coreDataFile[:-1]))
    coreDataDOM = minidom.parse(coreDataFile)
    
    entities = []
    domEntities = coreDataDOM.getElementsByTagName('entity')
    for domEntity in domEntities:
        className = str(domEntity.getAttributeNode('name').nodeValue)
        
        attributes = []
        relationships = []
        
        domAttributes = domEntity.getElementsByTagName('attribute')
        for domAttribute in domAttributes:
            attributes.append(__attributeDictionary(domAttribute))
        
        domRelationships = domEntity.getElementsByTagName('relationship')
        for domRelationship in domRelationships:
            relationships.append(__relationshipDictionary(domRelationship))
            
        parentName = 'Model'
        if domEntity.hasAttribute('parentEntity'):
            parentName = str(domEntity.getAttributeNode('parentEntity').nodeValue)
            
        currentEntity = domEntity
        while parentName != 'Model':
            parentEntity = None
            for possibleParentEntity in domEntities:
                if str(possibleParentEntity.getAttributeNode('name').nodeValue) == parentName:
                    parentEntity = possibleParentEntity
                    break
                    
            parentDOMAttributes = parentEntity.getElementsByTagName('attribute')
            for parentDOMAttribute in parentDOMAttributes:
                attributes.append(__attributeDictionary(parentDOMAttribute))
                
            parentDOMRelationships = parentEntity.getElementsByTagName('relationship')
            for parentDOMRelatinoship in parentDOMRelationships:
                relationships.append(__relationshipDictionary(parentDOMRelationship))
            
            currentEntity = parentEntity
            parentName = 'Model'
            if currentEntity.hasAttribute('parentEntity'):
                parentName = str(currentEntity.getAttributeNode('parentEntity').nodeValue)
                
        entity = {
            "className": className,
            "parentName": parentName,
            "attributes": attributes,
            "relationships": relationships,
            "primaryKey": primaryKey
        }
        
        endpoints = __endpointsList(className, attributes, relationships, primaryKey)
    
        entity.update({
            "endpoints": endpoints
        })
        
        entities.append(entity)
        
    return entities
        
def __attributeDictionary(domAttribute):
    attributeName = str(domAttribute.getAttributeNode('name').nodeValue)
               
    attributeType = "Undefined"
    sqlType = "VARCHAR"
    if domAttribute.hasAttribute('attributeType'):
       attributeType = str(domAttribute.getAttributeNode('attributeType').nodeValue)
       
    attributeIsOptional = True
    if domAttribute.hasAttribute('optional'):
       attributeIsOptional = str(domAttribute.getAttributeNode('optional').nodeValue) == 'YES'
    
    attributeDefaultValue = None
    if domAttribute.hasAttribute('defaultValueString'):
       attributeDefaultValue = str(domAttribute.getAttributeNode('defaultValueString').nodeValue)
       
    if "Integer" in attributeType:
       attributeDefaultValue = int(attributeDefaultValue) if (attributeDefaultValue != None) else 0
       sqlType = "INT"
    elif attributeType in ["Decimal", "Double", "Float"]:
       attributeDefaultValue = float(attributeDefaultValue) if (attributeDefaultValue != None) else 0.0
       sqlType = "DOUBLE"
    elif "Boolean" in attributeType:
       attributeDefaultValue = (attributeDefaultValue == 'YES') if (attributeDefaultValue != None) else False
       sqlType = "BOOL"
    elif "String" in attributeType:
       attributeDefaultValue = str(attributeDefaultValue) if (attributeDefaultValue != None) else "''"
    
    attribute = {
       "name": attributeName,
       "defaultValue": attributeDefaultValue,
       "canBeNull": attributeIsOptional
    }
       
    attribute.update({
        "sqlType": sqlType
    })
       
    return attribute
   
def __relationshipDictionary(domRelationship):
    relationshipName = str(domRelationship.getAttributeNode('name').nodeValue)
    
    relationshipInverseName = str(domRelationship.getAttributeNode('inverseName').nodeValue)
    relationshipType = str(domRelationship.getAttributeNode('destinationEntity').nodeValue)
    
    relationshipIsOptional = True
    if domRelationship.hasAttribute('optional'):
        relationshipIsOptional = str(domRelationship.getAttributeNode('optional').nodeValue) == 'YES'
        
    relationshipToMany = False
    if domRelationship.getAttributeNode('toMany'):
        relationshipToMany = str(domRelationship.getAttributeNode('toMany').nodeValue) == 'YES'
        
    relationship = {
        "name": relationshipName,
        "inverseName": relationshipInverseName,
        "toMany": relationshipToMany,
        "canBeNull": relationshipIsOptional
    }
    
    relationship.update({
        "sqlType": "VARCHAR" if not relationshipToMany else ""
    })
    
    return relationship
    
def __endpointsList(className, attributes, relationships, primaryKey):
    endpoints = []
    endpoints.append({
        "url": "/%ss/" % (className),
        "methods":
        [
            {
                "httpMethod": "GET",
                "parameters": [],
                "responses":
                [
                    {
                        "code": 200,
                        "description": "The query was successful."
                    }
                ]
            },
            {
                "httpMethod": "PUT",
                "parameters":
                [
                    {
                        "name": property['name'],
                        "description": "The %(className)s's %(propertyName)s." % ({
                            "className": className,
                            "propertyName": property['name']
                        })
                    }
                    
                    for property in (attributes + relationships)
                ],
                "responses":
                [
                    {
                        "code": 200,
                        "description": "The query was successful. The %(className)s was either added or updated." % ({
                            "className": className
                        })
                    }
                ]
            }
        ]
    })
    
    endpoints.append({
        "url": "/%ss/<%s>/" % (className, primaryKey),
        "methods":
        [
            {
                "httpMethod": "GET",
                "parameters":
                [
                    {
                        "name": primaryKey,
                        "description": "The %(primaryKey)s identifying the desired %(className)s." % ({
                            "primaryKey": primaryKey,
                            "className": className
                        })
                    }
                ],
                "responses":
                [
                    {
                        "code": 404,
                        "description": "The desired %(className)s was not found." % ({
                            "className": className
                        })
                    },
                    {
                        "code": 200,
                        "description": "The query was successful."
                    }
                ]
            },
            {
                "httpMethod": "POST",
                "parameters":
                [
                    {
                        "name": primaryKey,
                        "description": "The %(primaryKey)s identifying the desired %(className)s." % ({
                            "primaryKey": primaryKey,
                            "className": className
                        })
                    }
                ] +
                [
                    {
                        "name": property['name'],
                        "description": "The %(className)s's %(propertyName)s." % ({
                            "className": className,
                            "propertyName": property['name']
                        })
                    }
                    
                    for property in (attributes + relationships)
                ],
                "responses":
                [
                    {
                        "code": 404,
                        "description": "The desired %(className)s was not found." % ({
                            "className": className
                        })
                    },
                    {
                        "code": 200,
                        "description": "The query was successful. The %(className)s was updated." % ({
                            "className": className
                        })
                    }
                ]
            },
            {
                "httpMethod": "DELETE",
                "parameters":
                [
                    {
                        "name": primaryKey,
                        "description": "The %(primaryKey)s identifying the desired %(className)s." % ({
                            "primaryKey": primaryKey,
                            "className": className
                        })
                    }
                ],
                "responses":
                [
                    {
                        "code": 404,
                        "description": "The desired %(className)s was not found." % ({
                            "className": className
                        })
                    },
                    {
                        "code": 200,
                        "description": "The query was successful. The %(className)s was deleted." % ({
                            "className": className
                        })
                    }
                ]
            },
        ]
    })

    for attribute in attributes:
        endpoints.append({
            "url": "/%ss/<%s>/%s/" % (className, primaryKey, attribute['name']),
            "methods":
            [
                {
                    "httpMethod": "GET",
                    "parameters":
                    [
                        {
                            "name": primaryKey,
                            "description": "The %(primaryKey)s identifying the desired %(className)s." % ({
                                "primaryKey": primaryKey,
                                "className": className
                            })
                        }
                    ],
                    "responses":
                    [
                        {
                            "code": 404,
                            "description": "The desired %(className)s was not found." % ({
                                "className": className
                            })
                        },
                        {
                            "code": 200,
                            "description": "The query was successful."
                        }
                    ]
                },
                {
                    "httpMethod": "POST",
                    "parameters":
                    [
                        {
                            "name": primaryKey,
                            "description": "The %(primaryKey)s identifying the desired %(className)s." % ({
                                "primaryKey": primaryKey,
                                "className": className
                            })
                        },
                        {
                            'name': attribute['name'],
                            "description": "The %(className)s's %(propertyName)s." % ({
                                "className": className,
                                "propertyName": attribute['name']
                            })
                        }
                    ],
                    "responses":
                    [
                        {
                            "code": 404,
                            "description": "The desired %(className)s was not found." % ({
                                "className": className
                            })
                        },
                        {
                            "code": 200,
                            "description": "The query was successful. The %(className)s was updated." % ({
                                "className": className
                            })
                        }
                    ]
                }
            ]
        })
    
    for relationship in relationships:
       endpoints.append({
           "url": "/%ss/<%s>/%s/" % (className, primaryKey, relationship['name']),
           "methods":
           [
               {
                   "httpMethod": "GET",
                   "parameters":
                   [
                       {
                           "name": primaryKey,
                           "description": "The %(primaryKey)s identifying the desired %(className)s." % ({
                               "primaryKey": primaryKey,
                               "className": className
                           })
                       }
                   ],
                   "responses":
                   [
                       {
                           "code": 404,
                           "description": "The desired %(className)s was not found." % ({
                               "className": className
                           })
                       },
                       {
                           "code": 204,
                           "description": "The desired %(className)s does have any %(propertyName)s." % ({
                               "className": className,
                               "propertyName": relationship['name']
                           })
                       },
                       {
                           "code": 200,
                           "description": "The query was successful."
                       }
                   ]
               },
               {
                   "httpMethod": "POST",
                   "parameters":
                   [
                       {
                           "name": primaryKey,
                           "description": "The %(primaryKey)s identifying the desired %(className)s." % ({
                               "primaryKey": primaryKey,
                               "className": className
                           })
                       },
                       {
                           'name': relationship['name'],
                           "description": "The %(className)s's %(propertyName)s." % ({
                               "className": className,
                               "propertyName": relationship['name']
                           })
                       }
                   ],
                   "responses":
                   [
                       {
                           "code": 404,
                           "description": "The desired %(className)s was not found." % ({
                               "className": className
                           })
                       },
                       {
                           "code": 200,
                           "description": "The query was successful. The %(propertyName)s was added to the desired %(className)s." % ({
                               "className": className,
                               "propertyName": relationship['name']
                           })
                       }
                   ]
               }
           ]
       })
       
       if relationship['toMany']:
           endpoints[-1]['methods'].append({
               "httpMethod": "DELETE",
               "parameters":
               [
                   {
                       "name": primaryKey,
                       "description": "The %(primaryKey)s identifying the desired %(className)s." % ({
                           "primaryKey": primaryKey,
                           "className": className
                       })
                   },
                   {
                       'name': relationship['name'],
                       "description": "The %(className)s's %(propertyName)s to delete." % ({
                           "className": className,
                           "propertyName": relationship['name']
                       })
                   }
               ],
               "responses":
               [
                   {
                       "code": 404,
                       "description": "The desired %(className)s was not found." % ({
                           "className": className
                       })
                   },
                   {
                       "code": 200,
                       "description": "The query was successful. The %(className)s's %(propertyName)s was deleted." % ({
                           "className": className,
                           "propertyName": relationship['name']
                       })
                   }
               ]
           })