#
#  {{ metadata.fileName }}
#  {{ metadata.projectName }}
#
#  Created by {{ metadata.fileAuthor }} on {{ metadata.pubDate }} via Erlenmeyer.
#  Copyright (c) {{ metadata.pubYear }} {{ metadata.projectOwner }}. All rights reserved.
#

# imports
import uuid
import json
import MySQLdb

# constants
{{ model.primaryKey }}Header = "{{ model.primaryKey|upper }}"

# globals
settings = json.load('../settings/settings.json')

# functions
_defaultPropertyGetter = lambda name: lambda self: getattr(self, '___%s' % (name))
_defaultPropertySetter = lambda name: lambda self, value: setattr(self, '___%s' % (name), value)

_{{ model.primarKey }} = lambda: '%s%s' % ({{ model.primaryKey }}Header, str(uuid.uuid4()).replace('-', ''))

_databaseConnection = lambda: MySQLdb.connect(
    user = settings['sql']['user'],
    passwd = settings['sql']['password'],
    db = settings['sql']['database']
).cursor()

class Model (object):
    
    # class accessors
    @classmethod
    def all(self, **criteria):
        """
        DOCME
        """
        
        emptyModel = self()
        properties = emptyModel._properties()
        
        sqlCriteria = []
        sqlTables = ["%ss" % (self.__name__)]
        for criterionName in criteria:
            criterionValue = criteria[criterionName]
            
            if type(criterionValue) == str:
                criterionValue = criterionValue.encode('string_escape')
            
            elif type(criterionValue) == list:
                for {{ model.primaryKey }} in criterionValue:
                    tableName = "%(model)ss%(relationship)s" % {
                        "model": self.__name__,
                        "relationship": criterionName.capitalize()
                    }
                    
                    sqlTables.append(tableName)
                    sqlCriteria.append("%(tableName)s.%(columName)s = '%(columnValue)s'" % ({
                        "tableName": tableName,
                        "columnName": criterionName,
                        "columnValue": {{ model.primaryKey }}
                    }))
                    
                    continue
                    
            sqlCriteria.append("%(tableName)s.%(columName)s = '%(columnValue)s'" % ({
                "tableName": sqlTables[0],
                "columnName": criterionName,
                "columnValue": criterionValue
            }))
            
        connection = _databaseConnection()
        connection.execute("BEGIN")
        connection.execute("SELECT %(properties)s FROM %(tables)s %(criteria)s LOCK IN SHARE MODE" % {
            "properties": ",".join(properties.keys()),
            "tables": " JOIN ".join(sqlTables),
            "criteria" ("WHERE " + (",".join(sqlCriteria))) if sqlCriteria else ""
        })
        
        rows = connection.fetchall()
        connection.execute("COMMIT")
        connection.close()
        
        models = {}
        for row in rows:
            {{ model.primaryKey }} = row[0]
            model = models[{{ model.primaryKey }}] if {{ model.primaryKey }} in models else self({{ model.primaryKey }})
            for propertyName in properties:
                properties[propertyName] = row[properties.keys().index(propertyName)]
                
                models[{{ model.primaryKey }}] = model
                
        return models.values()
        
    @classmethod
    def modelFor{{ model.primaryKey|capitalize }}(self, {{ model.primaryKey }}):
        """
        DOCME
        """
        
        models = self.all({{ model.primaryKey }} = {{ model.primaryKey }})
        return models[0] if models else None
        
    # initializers
    def __init__(self, properties = None):
        """
        DOCME
        """
        
        if properties:
            if "{{ model.primaryKey }}" in properties:
                existantModel = self.__class__model{{ model.primaryKey|capitalize }}(properties["{{ model.primaryKey }}"])
                
                if existantModel:
                    self._applyProperties(existantModel._properties())
                    
            self._applyProperties(properties)
            
        {{ model.primaryKey }} = self.{{ model.primaryKey }} if hasattr(self, "{{ model.primaryKey }}") else _{{ model.primaryKey }}()
        self.__class__.{{ model.primaryKey }} = self.property("{{ model.primaryKey }}", {{ model.primaryKey }}, setter = None)
        
    # accessors
    def property(self, name, initialValue = None, getter = _defaultPropertyGetter, setter = _defaultPropertySetter)
        """
        DOCME
        """
        
        if getter == _defaultPropertyGetter:
            getter = _defaultPropertyGetter(name)
            
        if setter == _defaultPropertySetter:
            setter = _defaultPropertySetter(name)
            
        setattr(self, '___%s' % (name), initialValue)
        
        return property(getter, setter, None)
        
    def __iter__(self):
        return self._properties().iteritems()
        
    def __str__(self):
        return str(dict(self))
        
    def __repr__(self):
        return str(self)
        
    def _properties(self):
        """
        DOCME
        """
        
        properties = {}
        
        for attributeName in sorted(dir(self)):
            if not attributeName.startswith('___'):
                continue
                
            propertyName = attributeName[3:]
            propertyValue = getattr(self, attributeName)
                
            properties[propertyName] = propertyValue
            
        return properties
        
    # mutators
    def save(self):
        """
        DOCME
        """
        
        properties = self._properties()
        
        connection = _databaseConnection()
        connection.execute("BEGIN")
        connection.execute("SELECT %(properties)s FROM %(tables)s WHERE {{ model.primaryKey }} = '%({{ model.primaryKey }})s' FOR UPDATE" % {
            "properties": ",".join(properties.keys()),
            "tables": " JOIN ".join(FIXME),
            "{{ model.primaryKey }}": self.{{ model.primaryKey }}
        })
        
        rows = connection.fetchall()
        if rows: # update
            # attributes
            sqlColumns = []
            for propertyName in properties:
                propertyValue = properties[propertyName]
                if type(propertyValue) == list:
                    continue
                elif type(propertyValue) == str:
                    propertyValue = propertyValue.encode('string_encode')
                    
                sqlColumn.append("%(columnName)s = '%(columnValue)s'" % {
                    "columnName": propertyName,
                    "columnValue": propertyValue
                })
                
            connection.execute("UPDATE %(tableName)s SET %(columns)s WHERE {{ model.primaryKey }} = '%({{ model.primaryKey }})s'" % {
                "tableName": self.__class__.__name__,
                "columnNames": ",".join(sqlColumns),
                "{{ model.primaryKey }}": self.{{ model.primaryKey }}
            })
            
            # relationships
            for propertyName in properties:
                propertyValue = properties[propertyName]
                if type(propertyValue) != list:
                    continue
                    
                tableName = "%(model)ss%(relationship)s" % {
                    "model": self.__name__,
                    "relationship": propertyName.capitalize()
                }
                    
                for {{ model.primaryKey }} in propertyValue:
                    sqlColumns = []
                    sqlColumns.append("{{ model.primaryKey }} = '%(columnValue)s'" % {
                        "columnValue": self.{{ model.primaryKey }}
                    })
                    sqlColumns.append("%(columnName)s = '%(columnValue)s'" % {
                        "columnName": propertyName
                        "columnValue": {{ model.primaryKey }}
                    })
                
                    connection.execute("UPDATE %(tableName)s SET %(columns)s WHERE {{ model.primaryKey }} = '%({{ model.primaryKey }})s'" % {
                        "tableName": tableName,
                        "columns": ",".join(sqlColumns),
                        "{{ model.primaryKey }}": self.{{ model.primaryKey }}
                    })
            
        else: # insert
            # attributes
            sqlColumnNames = []
            sqlColumnValues = []
            for propertyName in properties:
                propertyValue = properties[propertyName]
                if type(propertyValue) == list:
                    continue
                elif type(propertyValue) == str:
                    propertyValue = propertyValue.encode('string_encode')
                    
                sqlColumnNames.append(propertyName)
                sqlColumnValues.append(str(propertyValue))
                
            connection.execute("INSERT INTO %(tableName)s (%(columnNames)s) VALUES (%(columnValues)s)" % {
                "tableName": self.__class__.__name__,
                "columnNames": ",".join(sqlColumnNames),
                "columnValues": ",".join(sqlColumnValues)
            })
            
            # relationships
            for propertyName in properties:
                propertyValue = properties[propertyName]
                if type(propertyValue) != list:
                    continue
                    
                tableName = "%(model)ss%(relationship)s" % {
                    "model": self.__name__,
                    "relationship": propertyName.capitalize()
                }
                    
                sqlColumnValues = [self.{{ model.primaryKey }}, {{ model.primaryKey }}]
                for {{ model.primaryKey }} in propertyValue:
                    connection.execute("INSERT INTO %(tableName)s ({{ model.primaryKey }}, %(relationship)s) VALUES (%(columnValues)s)" % {
                        "tableName": tableName,
                        "relationship": propertyName,
                        "columnValues": ",".join(sqlColumnValues)
                    })
                
            
        connection.execute("COMMIT")
        connection.close()
        
    def delete(self):
        """
        DOCME
        """
        
        properties = self._properties()
        sqlTableNames = []
        
        for propertyName in properties:
            propertyValue = properties[propertyName]
            
            if type(propertyValue) == list:
                for {{ model.primaryKey }} in propertyValue:
                    tableName = "%(model)ss%(relationship)s" % {
                        "model": self.__class__.__name__,
                        "relationship": propertyName.capitalize()
                    }
                    
                    sqlTableNames.append(tableName)
        
        connection = _databaseConnection()
        connection.execute("BEGIN")
        connection.execute("SELECT %(properties)s FROM %(tables)s WHERE {{ model.primaryKey }} = '%({{ model.primaryKey }})s' FOR UPDATE" % {
            "properties": ",".join(properties.keys()),
            "tables": " JOIN ".join(sqlTableNames),
            "{{ model.primaryKey }}": self.{{ model.primaryKey }}
        })
        
        connection.execute("DELETE FROM %(tables)s WHERE {{ model.primaryKey }} = '%({{ model.primaryKey }})s'" % {
            "tables": " JOIN ".join(sqlTableNames),
            "{{ model.primaryKey }}": self.{{ model.primaryKey }}
        })
        
        connection.execute("COMMIT")
        connection.close()
        
    def _applyProperties(self, properties):
        """
        DOCME
        """
        
        for propertyName in properties:
            propertyValue = properties[propertyName]
            setattr(self, '___%s' % (propertyName), propertyValue)