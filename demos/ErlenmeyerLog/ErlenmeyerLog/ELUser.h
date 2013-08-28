//
//  ELUser.h
//  ErlenmeyerLog
//
//  Created by Patrick Perini on 8/26/13.
//  Copyright (c) 2013 pcperini. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <CoreData/CoreData.h>

@class ELMessage;

@interface ELUser : NSManagedObject

@property (nonatomic, retain) NSString * uuid;
@property (nonatomic, retain) NSString * username;
@property (nonatomic, retain) NSSet *messages;
@end

@interface ELUser (CoreDataGeneratedAccessors)

- (void)addMessagesObject:(ELMessage *)value;
- (void)removeMessagesObject:(ELMessage *)value;
- (void)addMessages:(NSSet *)values;
- (void)removeMessages:(NSSet *)values;

@end