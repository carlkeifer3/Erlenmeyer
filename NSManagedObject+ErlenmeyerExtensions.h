//
//  NSManagedObject+ErlenmeyerExtensions.h
//  ErlenmeyerTests
//
//  Created by Patrick Perini on 2/11/13.
//  Copyright (c) 2013 MegaBits, LLC. All rights reserved.
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
 *  @param filters A set of key-value pairs to filter by.
 */
+ (void)allFromServer:(void(^)(NSArray *all, NSError *error))responseHandler where:(NSDictionary *)filters;

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

#pragma mark - Macros
/*!
 *  Creates a new enum with the given values, as well as string support for the values.
 *  @abstract enums cannot be effectively stored in CoreData. By using the ErlenmeyerPrimitiveTypeKey, Erlenmeyer can infer what kind of primitive (likely an enum) the value should be, and coerce that from number and string objects. Using the ErlenmeyerEnum macro to establish the enum creates the necessary string functions to support this behavior.
 */
#define ErlenmeyerEnum(EnumName, EnumValues...)                             \
    typedef enum                                                            \
    {                                                                       \
        EnumValues                                                          \
    } EnumName;                                                             \
                                                                            \
    static NSString *__Erlenmeyer##EnumName##Constants = @"" #EnumValues;   \
    __ErlenmeyerImplementation(EnumName)

/*!
 *  Creates NSDictionary pairings of numerical values and string names for the given enum.
 */
#define __ErlenmeyerImplementation(EnumName)                                                                                                \
    static NSDictionary *__Erlenmeyer##EnumName##ValuesByName()                                                                             \
    {                                                                                                                                       \
        NSArray *valueNameStrings = [__Erlenmeyer##EnumName##Constants componentsSeparatedByString: @","];                                  \
        NSMutableDictionary *valuesByName = [NSMutableDictionary dictionary];                                                               \
                                                                                                                                            \
        NSInteger lastValue = -1;                                                                                                           \
        for (NSString *valueNameString in valueNameStrings)                                                                                 \
        {                                                                                                                                   \
            NSArray *valueNamePair = [valueNameString componentsSeparatedByString: @"="];                                                   \
            NSString *name = [[valueNamePair objectAtIndex: 0] stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceCharacterSet]];    \
                                                                                                                                            \
            id value;                                                                                                                       \
            if ([valueNamePair count] > 1)                                                                                                  \
            {                                                                                                                               \
                value = [[valueNamePair objectAtIndex: 1] stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceCharacterSet]];         \
                lastValue = [value integerValue];                                                                                           \
            }                                                                                                                               \
            else                                                                                                                            \
            {                                                                                                                               \
                lastValue++;                                                                                                                \
            }                                                                                                                               \
            value = @(lastValue);                                                                                                           \
                                                                                                                                            \
            [valuesByName setObject: value forKey: name];                                                                                   \
        }                                                                                                                                   \
                                                                                                                                            \
        return (NSDictionary *)valuesByName;                                                                                                \
    }                                                                                                                                       \
                                                                                                                                            \
    static NSDictionary *__Erlenmeyer##EnumName##NamesByValue()                                                                             \
    {                                                                                                                                       \
        NSArray *valueNameStrings = [__Erlenmeyer##EnumName##Constants componentsSeparatedByString: @","];                                  \
        NSMutableDictionary *namesByValue = [NSMutableDictionary dictionary];                                                               \
                                                                                                                                            \
        NSInteger lastValue = -1;                                                                                                           \
        for (NSString *valueNameString in valueNameStrings)                                                                                 \
        {                                                                                                                                   \
            NSArray *valueNamePair = [valueNameString componentsSeparatedByString: @"="];                                                   \
            NSString *name = [[valueNamePair objectAtIndex: 0] stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceCharacterSet]];    \
                                                                                                                                            \
            id value;                                                                                                                       \
            if ([valueNamePair count] > 1)                                                                                                  \
            {                                                                                                                               \
                value = [[valueNamePair objectAtIndex: 1] stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceCharacterSet]];         \
                lastValue = [value integerValue];                                                                                           \
            }                                                                                                                               \
            else                                                                                                                            \
            {                                                                                                                               \
                lastValue++;                                                                                                                \
            }                                                                                                                               \
            value = @(lastValue);                                                                                                           \
                                                                                                                                            \
            [namesByValue setObject: name forKey: value];                                                                                   \
        }                                                                                                                                   \
                                                                                                                                            \
        return (NSDictionary *)namesByValue;                                                                                                \
    }                                                                                                                                       \
                                                                                                                                            \
    __ErlenmeyerEnumStringFunctions(EnumName)                                                                                               \
    __ErlenmeyerEnumNSStringExtensions(EnumName)

/*!
 *  Creates to/from string functions for values of the given enum. 
 */
#define __ErlenmeyerEnumStringFunctions(EnumName)                                       \
    static NSString *NSStringFrom##EnumName(EnumName value)                             \
    {                                                                                   \
        id valueObject = @(value);                                                      \
        return [__Erlenmeyer##EnumName##NamesByValue() objectForKey: valueObject];      \
    }                                                                                   \
                                                                                        \
    static EnumName EnumName##FromString(NSString *string)                              \
    {                                                                                   \
        id valueObject = [__Erlenmeyer##EnumName##ValuesByName() objectForKey: string]; \
        return (EnumName)[valueObject integerValue];                                    \
    }

/*!
 *  Creates NSString extension methods for values of the given enum.
 */
#define __ErlenmeyerEnumNSStringExtensions(EnumName)                    \
    @interface NSString (__ErlenmeyerEnum##EnumName##Extensions)        \
        - (EnumName)EnumName##Value;                                    \
        - (id)EnumName##ValueObject;                                    \
    @end                                                                \
    @implementation NSString (__ErlenmeyerEnum##EnumName##Extensions)   \
        - (EnumName)EnumName##Value                                     \
        {                                                               \
            return EnumName##FromString(self);                          \
        }                                                               \
                                                                        \
        - (id)EnumName##ValueObject                                     \
        {                                                               \
            return @([self EnumName##Value]);                           \
        }                                                               \
    @end