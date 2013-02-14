//
//  ErlenmeyerUser.h
//  NSManagedObject_ErlenmeyerTests
//
//  Created by Patrick Perini on 2/13/13.
//  Copyright (c) 2013 MegaBits. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <CoreData/CoreData.h>
#import "ErlenmeyerModel.h"

@class ErlenmeyerGroup, ErlenmeyerPost;

@interface ErlenmeyerUser : ErlenmeyerModel

@property (nonatomic, retain) NSString * email;
@property (nonatomic, retain) NSSet *groups;
@property (nonatomic, retain) NSSet *posts;
@end

@interface ErlenmeyerUser (CoreDataGeneratedAccessors)

- (void)addGroupsObject:(ErlenmeyerGroup *)value;
- (void)removeGroupsObject:(ErlenmeyerGroup *)value;
- (void)addGroups:(NSSet *)values;
- (void)removeGroups:(NSSet *)values;

- (void)addPostsObject:(ErlenmeyerPost *)value;
- (void)removePostsObject:(ErlenmeyerPost *)value;
- (void)addPosts:(NSSet *)values;
- (void)removePosts:(NSSet *)values;

@end
