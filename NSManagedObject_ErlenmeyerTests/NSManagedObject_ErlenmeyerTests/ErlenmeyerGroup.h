//
//  ErlenmeyerGroup.h
//  NSManagedObject_ErlenmeyerTests
//
//  Created by Patrick Perini on 2/13/13.
//  Copyright (c) 2013 MegaBits. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <CoreData/CoreData.h>
#import "ErlenmeyerModel.h"

@class ErlenmeyerUser;

@interface ErlenmeyerGroup : ErlenmeyerModel

@property (nonatomic, retain) NSSet *members;
@end

@interface ErlenmeyerGroup (CoreDataGeneratedAccessors)

- (void)addMembersObject:(ErlenmeyerUser *)value;
- (void)removeMembersObject:(ErlenmeyerUser *)value;
- (void)addMembers:(NSSet *)values;
- (void)removeMembers:(NSSet *)values;

@end
