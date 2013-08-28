//
//  ELUser+ELExtensions.m
//  ErlenmeyerLog
//
//  Created by Patrick Perini on 8/26/13.
//  Copyright (c) 2013 pcperini. All rights reserved.
//

#import "ELUser+ELExtensions.h"
#import "NSManagedObject+EKQueryingExtensions.h"

@implementation ELUser (ELExtensions)

+ (instancetype)userWithUsername:(NSString *)username
{
    for (id user in [self all])
    {
        if ([[user username] isEqualToString: username])
            return user;
    }
    
    id user = [[self alloc] init];
    [user setUuid: [[NSUUID UUID] UUIDString]];
    [user setUsername: username];
    return user;
}

- (NSArray *)messagesInChronologicalOrder
{
    return [[self messages] sortedArrayUsingDescriptors: @[[NSSortDescriptor sortDescriptorWithKey: @"timestamp"
                                                                                         ascending: YES]]];
}

@end
