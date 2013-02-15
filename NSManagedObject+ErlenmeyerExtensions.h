//
//  NSManagedObject+ErlenmeyerExtensions.h
//  ErlenmeyerTests
//
//  Created by Patrick Perini on 2/11/13.
//  Copyright (c) 2013 pcperini. All rights reserved.
//

#import <CoreData/CoreData.h>

@interface NSManagedObject (ErlenmeyerExtensions)

#pragma mark - Class Initializers
/*!
 *  This method needs to be called to initialize the internal machinations of the Erlenmeyer extensions.
 */
+ (void)initializeErlenmeyer;

#pragma mark - Class Accessors
/*!
 *  Returns the server URL used in all server requests.
 *  @result The server URL used in all server requests.
 */
+ (NSString *)serverURL;

/*!
 *  Returns the primary key of all NSManagedObjects.
 *  @result The primary key of all NSManagedObjects.
 */
+ (NSString *)primaryKey;

/*!
 *  Returns a new array containing all of the objects of this class.
 *  @result A new array containing all of the objects of this class.
 */
+ (NSArray *)all;

/*!
 *  Returns a new array containing all of the objects of this class.
 *  @param responseHandler A block that will recieve all objects from the server.
 */
+ (void)allFromServer:(void(^)(NSArray *all, NSError *error))responseHandler;

/*!
 *  Returns the value with the given identifier.
 *  @param anID The ID that is associated with the desired object.
 *  @result The value with the given ID.
 */
+ (id)get:(id)anID;

/*!
 *  Returns the value with the given identifier.
 *  @param anID The ID that is associated with the desired object.
 *  @param responseHandler A block that will recieve the object from the server.
 */
+ (void)get:(id)anID fromServer:(void(^)(id object, NSError *error))responseHandler;

#pragma mark - Class Mutators
/*!
 *  Sets the server URL used in all server requests.
 *  @param serverURL The server URL used in all server requests.
 */
+ (void)setServerURL:(NSString *)serverURL;

/*!
 *  Sets the primary key of all NSManagedObjects.
 *  @param primaryKey The primary key of all NSManagedObjects.
 */
+ (void)setPrimaryKey:(NSString *)primaryKey;

#pragma mark - Accessors
/*!
 *  Returns a dictionary of key/value pairs that represents the receiver.
 *  @result A dictionary of key/values pairs that represents the receiver.
 *  @discussion Relationships are represented by references to IDs.
 */
- (NSDictionary *)dictionaryValue;

#pragma mark - Mutators
/*!
 *  Adds to the receiving dictionary the entries from another dictionary.
 *  @param dictionary The dictionary from which to add entries.
 */
- (void)addEntriesFromDictionary:(NSDictionary *)dictionary;

/*!
 *  Attempts to commit unsaved changes to NSManagedObjects in their persistent store. Note that this saves all NSManagedObjects.
 */
- (void)save;

/*!
 *  Commits unsaved changes to the reciever in the server.
 */
- (void)saveToServer:(void(^)(NSError *error))responseHandler;

/*!
 *  Removes the receiver.
 */
- (void)delete;

/*!
 *  Removes the receiver from the server.
 */
- (void)deleteFromServer:(void(^)(NSError *error))responseHandler;

/*!
 *  Retrieves receiver's data from a fault.
 */
- (void)realizeFromFault;

@end