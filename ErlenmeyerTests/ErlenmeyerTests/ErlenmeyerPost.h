//
//  ErlenmeyerPost.h
//  ErlenmeyerTests
//
//  Created by Patrick Perini on 2/14/13.
//  Copyright (c) 2013 MegaBits. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <CoreData/CoreData.h>
#import "ErlenmeyerModel.h"

@class ErlenmeyerUser;

@interface ErlenmeyerPost : ErlenmeyerModel

@property (nonatomic, retain) NSString * text;
@property (nonatomic, retain) ErlenmeyerUser *author;

@end
