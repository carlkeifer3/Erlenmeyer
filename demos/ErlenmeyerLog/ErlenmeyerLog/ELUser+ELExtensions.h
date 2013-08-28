//
//  ELUser+ELExtensions.h
//  ErlenmeyerLog
//
//  Created by Patrick Perini on 8/26/13.
//  Copyright (c) 2013 pcperini. All rights reserved.
//

#import "ELUser.h"

@interface ELUser (ELExtensions)

+ (instancetype)userWithUsername:(NSString *)username;
- (NSArray *)messagesInChronologicalOrder;

@end
