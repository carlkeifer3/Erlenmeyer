#
#  {{ metadata.fileName }}
#  {{ metadata.projectName }}
#
#  Created by {{ metadata.fileAuthor }} on {{ metadata.pubDate }}.
#  Copyright (c) {{ metadata.pubYear }} {{ metadata.projectOwner }}. All rights reserved.
#

# imports
import uuid
import json
import MySQLdb

# constants
{{ model.primaryKey }}Header = "{{ model.primaryKey|upper }}"

# globals
__sqlSettings = {}

# functions
_defaultPropertyGetter = lambda name: lambda self: getattr(self, '___%s' % (name))
_defaultPropertySetter = lambda name: lambda self, value: setattr(self, '___%s' % (name), value)

_{{ model.primaryKey }} = lambda: '%s%s' % ({{ model.primaryKey }}Header, str(uuid.uuid4()).replace('-', ''))

def _databaseConnection(settingsFile = "../settings/settings.json"):
    if not __sqlSettings:
        settings = json.load(open(settingsFile))
        __sqlSettings = settings["sql"]
    
    database = MySQLdb.connect(
        user = __sqlSettings["user"],
        passwd = __sqlSettings["password"],
        db = __sqlSettings["database"]
    )
    
    return database.cursor()

class Model (object):

    # class accessors
    @classmethod
    def all(self, **criteria):
        
        emptyModel = self()
        properties = emptyModel.__properties()
        
        sqlCriteria = []
        sqlTables = ["%ss" % (self.__name__)]
        for criterionName in criteria:
            criterionValue = criteria[criterionName]
            if type(criterionValue) == str:
                criterionValue = criterionValue.encode('string_escape')
            
            elif type(criterionValue) == list:
                for {{ model.primaryKey }} in criterionValue:
                    sqlCriteria.append("%s = '%s'" % (
                        criterionName,
                        model.primaryKey
                    ))
                
                sqlTables.append("%(model)ss%(relationship)s" % {
                    self.__name__,
                    criterionName.capitalize()
                })
                
                continue
                
            sqlCriteria.append("%s = '%s'" % (
                criterionName,
                criterionValue
            ))
            
        connection = _databaseConnection()
        connection.execute("BEGIN")
        connection.execute("SELECT %(properties)s FROM %(tables)s %(criteria)s LOCK IN SHARE MODE" % {
            "properties": ",".join(properties.keys()),
            "tables": " JOIN ".join(sqlTables),
            "criteria": "WHERE " + ",".join(sqlCriteria) if sqlCriteria else ""
        })
        
        rows = connection.fetchall()
        models = {}
        
        connection.execute("COMMIT")
        connection.close()
        
        for row in rows:
            model = models[row[0]] if row[0] in models else self(row[0])
            model.__applyProperties(properties, row[1:])
            
            models[row[0]] = model
            
        return models.values()
        
    @classmethod
    def objectFor{{ model.primaryKey|capitalize }}(self, {{ model.primaryKey }}):
        models = self.all({{ model.primaryKey }} = {{ model.primaryKey }})
        return models[0] if len(models) > 0 else None
        
    # initializers
    def __init__(self, dictionary = None):
        if dictionary:
            if "{{ model.primaryKey }}" in dictionary:
                existantModel = self.__class__.objectFor{{ model.primaryKey|capitalize }}(dictionary["{{ model.primaryKey }}"])
                
                if existantModel:
                    self.__applyProperties(self.__properties(), existantModel.__properties().values())
                    return
                
            columns = [dictionary[propertyName] for propertyName in self.__properties()]
            self.__applyProperties(self.__properties(), columns)
            
        {{ model.primaryKey }} = getattr(self, "___{{ model.primaryKey }}", None)
        self.__class__.{{ model.primaryKey }} = self.property("{{ model.primaryKey }}", {{ model.primaryKey }}, setter = None)        
        
    # accessors
    def property(self, name, initialValue = None, getter = _defaultPropertyGetter, setter = _defaultPropertySetter):
        
        if getter == _defaultPropertyGetter:
            getter = _defaultPropertyGetter(name)
            
        if setter == _defaultPropertySetter:
            setter = _defaultPropertySetter(name)
            
        setattr(self, '___%s' % (name), initialValue)
        
        return property(getter, setter, None)
    
    def __iter__(self):
        properties = self.__properties()
        for propertyName in properties:
            yield (propertyName, properties[propertyName])
            
    def __str__(self):
        return str(dict(self))
        
    def __repr__(self):
        return str(self)
        
    def __properties(self):
        properties = {}
        
        for attributeName in sorted(dir(self)):
            if not attributeName.startswith('___'):
                continue
                
            propertyName = attributeName[3:]
            
            propertyValue = getattr(self, attributeName)
            if type(propertyValue) == str:
                propertyValue = propertyValue.encode('string_escape')
                
            properties[propertyName] = propertyValue
            
        return properties
        
    # mutators
    def save(self):
        pass
        
    def delete(self):
        pass
        
    def __applyProperties(self, properties, columns):
        propertyNames = ['___%s' % (propertyName) for propertyName in properties]
        
        for propertyIndex in range(len(columns)):
            propertyName = propertyNames[propertyIndex]
            
            propertyValue = columns[propertyIndex]
            if type(propertyValue) == str:
                propertyValue = propertyValue.decode('string_escape')
                
            if type(properties[propretyIndex]) == list:
                getattr(self, propertyName).append(propertyValue)
            else:
                setattr(self, propertyName, propertyValue)