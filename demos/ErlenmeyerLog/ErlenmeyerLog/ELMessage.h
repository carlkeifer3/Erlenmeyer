//
//  ELMessage.h
//  ErlenmeyerLog
//
//  Created by Patrick Perini on 8/26/13.
//  Copyright (c) 2013 pcperini. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <CoreData/CoreData.h>

@class ELUser;

@interface ELMessage : NSManagedObject

@property (nonatomic, retain) NSString * uuid;
@property (nonatomic, retain) NSString * text;
@property (nonatomic, retain) NSNumber * timestamp;
@property (nonatomic, retain) ELUser *author;

@end
