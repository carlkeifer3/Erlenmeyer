//
//  NSManagedObject+ErlenmeyerExtensions.m
//  ErlenmeyerTests
//
//  Created by Patrick Perini on 2/11/13.
//  Copyright (c) 2013 pcperini. All rights reserved.
//

#import "NSManagedObject+ErlenmeyerExtensions.h"
#import "PCHTTP.h"
#import <objc/runtime.h>

#pragma mark - Internal Constants
NSString *const ErlenmeyerDefaultServerURL = @"http://127.0.0.1:8080";
NSString *const ErlenmeyerDefaultPrimaryKey = @"uuid";

NSString *const ErlenmeyerErrorDomain = @"NSManagedObjectErlenmeyerErrorDomain";

#pragma mark - Globals
static NSString *serverURL;
static NSString *primaryKey;
static NSManagedObjectContext *managedObjectContext;
static NSManagedObjectModel *managedObjectModel;
static NSPersistentStoreCoordinator *persistentStoreCoordinator;

@interface NSManagedObject (ErlenmeyerPrivateExtensions)

#pragma mark - Properties
@property (nonatomic) BOOL existsInServer;
@property (nonatomic, readonly) NSMutableDictionary *changedValuesForServer;

#pragma mark - Class Accessors
+ (NSArray *)allMatchingPredicate:(NSString *)predicateString limit:(NSInteger)limit;

#pragma mark - Class Error Handlers
+ (void)throwExceptionForError:(NSError *)error;

#pragma mark - Responders
- (void)objectsDidChange:(NSNotification *)notification;

@end

@implementation NSManagedObject (ErlenmeyerExtensions)

#pragma mark - Class Initializers
+ (void)initialize
{
    if (!serverURL)
    {
        serverURL = ErlenmeyerDefaultServerURL;
    }
    
    if (!primaryKey)
    {
        primaryKey = ErlenmeyerDefaultPrimaryKey;
    }
    
    if (!managedObjectModel)
    {
        managedObjectModel = [NSManagedObjectModel mergedModelFromBundles: nil];
    }
    
    if (!persistentStoreCoordinator)
    {
        NSURL *applicationDocumentsDirectory = [[[NSFileManager defaultManager] URLsForDirectory: NSDocumentDirectory
                                                                                       inDomains: NSUserDomainMask] lastObject];
        NSURL *storeURL = [applicationDocumentsDirectory URLByAppendingPathComponent: @"NSManagedObjects.sqlite"];
        
        NSError *error;
        persistentStoreCoordinator = [[NSPersistentStoreCoordinator alloc] initWithManagedObjectModel: managedObjectModel];
        [persistentStoreCoordinator addPersistentStoreWithType: NSSQLiteStoreType
                                                 configuration: nil
                                                           URL: storeURL
                                                       options: nil
                                                         error: &error];
        [self throwExceptionForError: error];
    }
    
    if (!managedObjectContext)
    {
        managedObjectContext = [[NSManagedObjectContext alloc] init];
        [managedObjectContext setPersistentStoreCoordinator: persistentStoreCoordinator];
    }
}

#pragma mark - Class Accessors
+ (NSString *)serverURL
{
    return serverURL;
}

+ (NSString *)primaryKey
{
    return primaryKey;
}

+ (NSArray *)all
{
    return [self allMatchingPredicate: nil limit: 0];
}

+ (void)allFromServer:(void (^)(NSArray *, NSError *))responseHandler
{
    PCHTTPResponseBlock getAllResponse = ^(PCHTTPResponse *response)
    {
        NSError *error;
        NSArray *all;
        
        switch ([response status])
        {
            case PCHTTPResponseStatusNotFound:
            {
                error = [NSError errorWithDomain: ErlenmeyerErrorDomain
                                            code: PCHTTPResponseStatusNotFound
                                        userInfo: nil];
                break;
            }
                
            case PCHTTPResponseStatusOK:
            {
                all = [response object];
                break;
            }
        }
    
        responseHandler(all, error);
    };
    
    NSString *getAllURL = [NSString stringWithFormat: @"%@/%@s", serverURL, NSStringFromClass(self)];
    [PCHTTPClient get: getAllURL responseHandler: getAllResponse];
}

+ (NSArray *)allMatchingPredicate:(NSString *)predicateString limit:(NSInteger)limit
{
    NSEntityDescription *entityDescription = [NSEntityDescription entityForName: NSStringFromClass(self)
                                                         inManagedObjectContext: managedObjectContext];
    
    NSFetchRequest *fetchRequest = [[NSFetchRequest alloc] init];
    [fetchRequest setEntity: entityDescription];
    
    if (predicateString)
    {
        NSPredicate *predicate = [NSPredicate predicateWithFormat: predicateString];
        [fetchRequest setPredicate: predicate];
    }
    
    [fetchRequest setFetchLimit: limit];
    
    NSError *error;
    NSArray *results = [managedObjectContext executeFetchRequest: fetchRequest
                                                           error: &error];
    [self throwExceptionForError: error];
    
    return results;
}

+ (NSManagedObject *)get:(id)anID
{
    NSString *predicateString = [NSString stringWithFormat:@"%@ == \"%@\"", primaryKey, anID];
    NSArray *results = [self allMatchingPredicate: predicateString limit: 1];
    
    if ([results count] > 0)
        return [results objectAtIndex: 0];
    
    return nil;
}

+ (void)get:(id)anID fromServer:(void (^)(NSManagedObject *, NSError *))responseHandler
{
    NSManagedObject *object = [[self alloc] init];
    PCHTTPBatchClient *batchClient = [[PCHTTPBatchClient alloc] init];
    
    NSString *getURL = [NSString stringWithFormat: @"%@/%@s/%@", serverURL, NSStringFromClass(self), anID];
    [batchClient addGetRequest: getURL];
    
    // Add relationships
    for (NSString *relationshipName in [[object entity] relationshipsByName])
    {
        NSRelationshipDescription *relationshipDescription = [[[object entity] relationshipsByName] objectForKey: relationshipName];
        if (![relationshipDescription isToMany])
            continue;
        
        NSString *getRelationshipURL = [NSString stringWithFormat: @"%@/%@", getURL, relationshipName];
        [batchClient addGetRequest: getRelationshipURL];
    }
    
    PCHTTPBatchResponseBlock getResponse = ^(NSArray *responses)
    {
        NSError *error;
        NSDictionary *objectDictionary;
        
        for (PCHTTPResponse *response in responses)
        {
            if ([responses indexOfObject: response] == 0)
            {
                switch ([response status])
                {
                    case PCHTTPResponseStatusNotFound:
                    {
                        error = [NSError errorWithDomain: ErlenmeyerErrorDomain
                                                    code: PCHTTPResponseStatusNotFound
                                                userInfo: nil];
                        
                        responseHandler(nil, error);
                        return;
                    }
                        
                    case PCHTTPResponseStatusOK:
                    {
                        objectDictionary = [response object];
                        break;
                    }
                }
                
                [object addEntriesFromDictionary: objectDictionary];
                continue;
            }
        
            // Add relationships
            NSArray *relationshipDictionaries;
            NSString *relationshipName = [[response requestURL] lastPathComponent];
            switch ([response status])
            {
                case PCHTTPResponseStatusNotFound:
                {
                    error = [NSError errorWithDomain: ErlenmeyerErrorDomain
                                                code: PCHTTPResponseStatusNotFound
                                            userInfo: nil];
                    
                    responseHandler(nil, error);
                    return;
                }
                    
                case PCHTTPResponseStatusOK:
                {
                    relationshipDictionaries = [response object];
                    break;
                }
                    
                NSRelationshipDescription *relationshipDescription = [[[object  entity] relationshipsByName] objectForKey: relationshipName];
                for (NSDictionary *relationshipDictionary in relationshipDictionaries)
                {
                    Class relationshipClass = NSClassFromString([[relationshipDescription destinationEntity] managedObjectClassName]);
                    NSManagedObject *relationshipObject = [[relationshipClass alloc] init];
                    [relationshipObject addEntriesFromDictionary: relationshipDictionary];
                    
                    [[object mutableSetValueForKey: relationshipName] addObject: relationshipObject];
                }
            }
        }
    };

    [batchClient performRequestsWithResponseHandler: getResponse];
}

#pragma mark - Class Mutators
+ (void)setServerURL:(NSString *)aURL
{
    serverURL = [aURL copy];
}

+ (void)setPrimaryKey:(NSString *)aKey
{
    primaryKey = [aKey copy];
}

#pragma mark - Class Error Handlers
+ (void)throwExceptionForError:(NSError *)error
{
    if (!error)
        return;
    
    NSException *errorException = [NSException exceptionWithName: [error domain]
                                                          reason: [error localizedDescription]
                                                        userInfo: [error userInfo]];
    [errorException raise];
}

#pragma mark - Initializers
- (id)init
{
    self = [super init];
    if (!self)
        return nil;
    
    NSMutableDictionary *changedValuesForServer = [NSMutableDictionary dictionary];
    [changedValuesForServer setValue: [NSMutableArray array]
                              forKey: NSInsertedObjectsKey];
    [changedValuesForServer setValue: [NSMutableArray array]
                              forKey: NSDeletedObjectsKey];
    objc_setAssociatedObject(self, "changedValuesForServer", changedValuesForServer,  OBJC_ASSOCIATION_COPY);
    
    [[NSNotificationCenter defaultCenter] addObserver: self
                                             selector: @selector(objectsDidChange:)
                                                 name: NSManagedObjectContextObjectsDidChangeNotification
                                               object: nil];
    
    return self;
}

#pragma mark - Deallocators
- (void)dealloc
{
    [[NSNotificationCenter defaultCenter] removeObserver: self];
}

#pragma mark - Accessors
- (BOOL)existsInServer
{
    return [objc_getAssociatedObject(self, "existsInServer") boolValue];
}

- (NSMutableDictionary *)changedValuesForServer
{
    return objc_getAssociatedObject(self, "changedValuesForServer");
}

- (NSDictionary *)dictionaryValue
{
    NSMutableDictionary *dictionaryValue = [NSMutableDictionary dictionary];
    
    // Add attributes
    for (NSString *attributeName in [[self entity] attributesByName])
    {
        id attributeValue = [self valueForKey: attributeName];
        
        if (!attributeValue)
        {
            attributeValue = [NSNull null];
        }
        
        if ([attributeValue isKindOfClass: [NSData class]])
        {
            attributeValue = [[NSString alloc] initWithData: attributeValue
                                                   encoding: NSUTF8StringEncoding];
        }
        
        [dictionaryValue setObject: attributeValue
                            forKey: attributeName];
    }
    
    // Add relationships
    for (NSString *relationshipName in [[self entity] relationshipsByName])
    {
        NSRelationshipDescription *relationshipDescription = [[[self entity] relationshipsByName] objectForKey: relationshipName];
        
        if ([relationshipDescription isToMany])
        {
            NSMutableArray *objects = [NSMutableArray array];
            for (NSManagedObject *object in [self valueForKey: relationshipName])
            {
                id objectID = [object valueForKey: primaryKey];
                if (!objectID)
                    continue;
                
                [objects addObject: objectID];
            }
            
            [dictionaryValue setObject: objects
                                forKey: relationshipName];
        }
        else
        {
            NSManagedObject *object = [self valueForKey: relationshipName];
            id relationshipID = [object valueForKey: primaryKey];
            
            if (!relationshipID)
            {
                relationshipID = [NSNull null];
            }
            
            [dictionaryValue setObject: relationshipID
                                forKey: relationshipName];
        }
    }
    
    return (NSDictionary *)dictionaryValue;
}

#pragma mark - Mutators
- (void)setExistsInServer:(BOOL)existsInServer
{
    objc_setAssociatedObject(self, "existsInServer", @(existsInServer), OBJC_ASSOCIATION_ASSIGN);
}

- (void)addEntriesFromDictionary:(NSDictionary *)dictionary
{
    for (NSString *key in dictionary)
    {
        id value = [dictionary objectForKey: key];
        if ([value isKindOfClass: [NSNull class]])
            continue;
        
        if ([value isKindOfClass: [NSArray class]])
        {
            for (id objectID in value)
            {
                NSManagedObject *object = [NSManagedObject get: objectID];
                [[self mutableSetValueForKey: key] addObject: object];
            }
            
            continue;
        }
        
        if ([[self valueForKey: key] isKindOfClass: [NSManagedObject class]])
        {
            value = [NSManagedObject get: value];
        }
        
        [self setValue: value
                forKey: key];
    }
}

- (void)save
{
    if ([managedObjectContext hasChanges])
    {
        NSError *error;
        [managedObjectContext save: &error];
        [[self class] throwExceptionForError: error];
    }
}

- (void)saveToServer:(void (^)(NSError *))responseHandler
{
    PCHTTPBatchClient *batchClient = [[PCHTTPBatchClient alloc] init];
    
    NSString *putURL = [NSString stringWithFormat: @"%@/%@s", serverURL, NSStringFromClass([self class])];
    NSString *postURL = [NSString stringWithFormat: @"%@/%@", putURL, [self valueForKey: primaryKey]];
    
    if ([self existsInServer])
    {
        [batchClient addPostRequest: postURL
                            payload: [self dictionaryValue]];
    }
    else
    {
        [batchClient addPutRequest: putURL
                           payload: [self dictionaryValue]];
    }

    // Add relationships
    for (NSString *relationshipName in [[self entity] relationshipsByName])
    {
        NSRelationshipDescription *relationshipDescription = [[[self entity] relationshipsByName] objectForKey: relationshipName];
        if (![relationshipDescription isToMany])
        {
            NSString *postRelationshipURL = [NSString stringWithFormat: @"%@/%@", postURL, relationshipName];
            NSDictionary *postRelationshipPayload = @{
                [NSString stringWithFormat: @"%@Object", relationshipName]: [[self valueForKey: relationshipName] valueForKey: primaryKey]
            };
            
            [batchClient addPostRequest: postRelationshipURL
                                payload: postRelationshipPayload];
            continue;
        }
        
        for (NSManagedObject *relationshipObject in [self valueForKey: relationshipName])
        {
            if ([[[self changedValuesForServer] objectForKey: NSInsertedObjectsKey] containsObject: relationshipObject])
            {
                NSString *putRelationshipURL = [NSString stringWithFormat: @"%@/%@", postURL, relationshipName];
                NSDictionary *putRelationshipPayload = @{
                    [NSString stringWithFormat: @"%@Object", relationshipName]: [relationshipObject valueForKey: primaryKey]
                };
                
                [batchClient addPutRequest: putRelationshipURL
                                   payload: putRelationshipPayload];
            }
            else if ([[[self changedValuesForServer] objectForKey: NSDeletedObjectsKey] containsObject: relationshipObject])
            {
                NSString *deleteRelationshipURL = [NSString stringWithFormat: @"%@/%@", postURL, relationshipName];
                NSDictionary *deleteRelationshipParameters = @{
                    [NSString stringWithFormat: @"%@Object", relationshipName]: [relationshipObject valueForKey: primaryKey]
                };
                
                [batchClient addPutRequest: deleteRelationshipURL
                                parameters: deleteRelationshipParameters];
            }
        }
    }
    
    [[self changedValuesForServer] setObject: [NSMutableArray array]
                                      forKey: NSInsertedObjectsKey];
    [[self changedValuesForServer] setObject: [NSMutableArray array]
                                      forKey: NSDeletedObjectsKey];
    
    PCHTTPBatchResponseBlock saveResponse = ^(NSArray *responses)
    {
        NSError *error;
        for (PCHTTPResponse *response in responses)
        {
            switch ([response status])
            {
                case PCHTTPResponseStatusBadRequest:
                {
                    error = [NSError errorWithDomain: ErlenmeyerErrorDomain
                                                code: PCHTTPResponseStatusBadRequest
                                            userInfo: nil];
                    
                    responseHandler(error);
                    return;
                }
                    
                case PCHTTPResponseStatusNotFound:
                {
                    error = [NSError errorWithDomain: ErlenmeyerErrorDomain
                                                code: PCHTTPResponseStatusNotFound
                                            userInfo: nil];
                    
                    responseHandler(error);
                    return;
                }
            }
        }
        
        responseHandler(error);
    };

    [batchClient performRequestsWithResponseHandler: saveResponse];
}

- (void)delete:(id)sender
{
    [managedObjectContext delete: self];
}

- (void)deleteFromServer:(void (^)(NSError *))responseHandler
{
    PCHTTPResponseBlock deleteResponse = ^(PCHTTPResponse *response)
    {
        NSError *error;
        
        switch ([response status])
        {
            case PCHTTPResponseStatusNotFound:
            {
                error = [NSError errorWithDomain: ErlenmeyerErrorDomain
                                            code: PCHTTPResponseStatusNotFound
                                        userInfo: nil];
                break;
            }
        }
        
        responseHandler(error);
    };
    
    NSString *deleteURL = [NSString stringWithFormat: @"%@/%@s/%@", serverURL, NSStringFromClass([self class]), [self valueForKey: primaryKey]];
    [PCHTTPClient delete: deleteURL responseHandler: deleteResponse];
}

#pragma mark - Responders
- (void)objectsDidChange:(NSNotification *)notification
{
    if ([notification object] != self)
        return;
    
    NSArray *insertedObjects = [[notification userInfo] objectForKey: NSInsertedObjectsKey];
    [[[self changedValuesForServer] objectForKey: NSInsertedObjectsKey] addObjectsFromArray: insertedObjects];
    
    NSArray *deletedObjects = [[notification userInfo] objectForKey: NSDeletedObjectsKey];
    [[[self changedValuesForServer] objectForKey: NSDeletedObjectsKey] addObjectsFromArray: deletedObjects];
}

@end
