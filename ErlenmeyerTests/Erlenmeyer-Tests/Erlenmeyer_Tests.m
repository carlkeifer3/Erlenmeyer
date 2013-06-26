//
//  Erlenmeyer_Tests.m
//  Erlenmeyer-Tests
//
//  Created by Patrick Perini on 6/22/13.
//  Copyright (c) 2013 MegaBits. All rights reserved.
//

#import <XCTest/XCTest.h>
#import <CoreData/CoreData.h>
#import "NSManagedObject+ErlenmeyerExtensions.h"
#import "ErlenmeyerModel.h"
#import "ErlenmeyerPost.h"
#import "ErlenmeyerGroup.h"
#import "ErlenmeyerUser.h"

@interface Erlenmeyer_Tests : XCTestCase

@end

@implementation Erlenmeyer_Tests

- (void)setUp
{
    [super setUp];
    [NSManagedObject setServerURL: @"http://127.0.0.1:5000"]; // FIXME
}

#pragma mark - Local Models
- (void)testModelCreation
{
    ErlenmeyerModel *newModel = [[ErlenmeyerModel alloc] init];
    [newModel setUuid: [[NSUUID UUID] description]];
    
    XCTAssertNotNil(newModel, @"%s: newModel (%p) is nil", __PRETTY_FUNCTION__, newModel);
    XCTAssertNotNil([newModel uuid], @"%s: [newModel uuid] (%p) is nil", __PRETTY_FUNCTION__, [newModel uuid]);
}

- (void)testUserCreation
{
    ErlenmeyerUser *newUser = [[ErlenmeyerUser alloc] init];
    [newUser setUuid: [[NSUUID UUID] description]];
    [newUser setEmail: @"test@megabitsapp.com"];
    
    XCTAssertNotNil(newUser, @"%s: newUser (%p) is nil", __PRETTY_FUNCTION__, newUser);
    XCTAssertNotNil([newUser uuid], @"%s: [newUser uuid] (%p) is nil", __PRETTY_FUNCTION__, [newUser uuid]);
    XCTAssertNotNil([newUser email], @"%s: [newUser email] (%p) is nil", __PRETTY_FUNCTION__, [newUser email]);
}

- (void)testPostCreation
{
    ErlenmeyerPost *newPost = [[ErlenmeyerPost alloc] init];
    [newPost setUuid: [[NSUUID UUID] description]];
    [newPost setText: @"This is a new post!"];
    
    XCTAssertNotNil(newPost, @"%s: newPost (%p) is nil", __PRETTY_FUNCTION__, newPost);
    XCTAssertNotNil([newPost uuid], @"%s: [newPost uuid] (%p) is nil", __PRETTY_FUNCTION__, [newPost uuid]);
    XCTAssertNotNil([newPost text], @"%s: [newPost text] (%p) is nil", __PRETTY_FUNCTION__, [newPost text]);
    
    ErlenmeyerUser *newUser = [[ErlenmeyerUser alloc] init];
    [newUser setUuid: [[NSUUID UUID] description]];
    [newUser setEmail: @"test@megabitsapp.com"];
    [newPost setAuthor: newUser];
    
    XCTAssertEquals(newUser, [newPost author], @"%s: [newPost author] (%p) != newUser (%p)", __PRETTY_FUNCTION__, [newPost author], newUser);
}

- (void)testGroupCreation
{
    ErlenmeyerGroup *newGroup = [[ErlenmeyerGroup alloc] init];
    [newGroup setUuid: [[NSUUID UUID] description]];
    
    XCTAssertNotNil(newGroup, @"%s: newGroup (%p) is nil", __PRETTY_FUNCTION__, newGroup);
    XCTAssertNotNil([newGroup uuid], @"%s: [newGroup uuid] (%p) is nil", __PRETTY_FUNCTION__, [newGroup uuid]);
    
    ErlenmeyerUser *newUser = [[ErlenmeyerUser alloc] init];
    [newUser setUuid: [[NSUUID UUID] description]];
    [newUser setEmail: @"test@megabitsapp.com"];
    [newGroup addMembersObject: newUser];
    
    XCTAssertTrue([[newGroup members] containsObject: newUser], @"%s: newUser (%p) not in [newGroup members] (%p, %@)", __PRETTY_FUNCTION__, newUser, [newGroup members], [newGroup members]);
}

#pragma mark - Local Database Deletion
- (void)testUserLocalDeletion
{
    ErlenmeyerUser *newUser = [[ErlenmeyerUser alloc] init];
    [newUser setUuid: [[NSUUID UUID] description]];
    [newUser setEmail: @"test@megabitsapp.com"];
    
    [newUser save];
    
    [NSManagedObject deleteAll];
    NSArray *users = [ErlenmeyerUser all];
    
    XCTAssertTrue([users count] <= 0, @"%s: [users count] == %d", __PRETTY_FUNCTION__, [users count]);
}

#pragma mark - Local Database Input
- (void)testUserLocalSaving
{    
    ErlenmeyerUser *newUser = [[ErlenmeyerUser alloc] init];
    [newUser setUuid: [[NSUUID UUID] description]];
    [newUser setEmail: @"test@megabitsapp.com"];
    
    [newUser save];
    
    XCTAssertFalse([newUser hasChanges], @"%s: newUser (%p) has changes: %@", __PRETTY_FUNCTION__, newUser, [newUser changedValuesForCurrentEvent]);

    [NSManagedObject deleteAll];
}

- (void)testPostLocalSaving
{
    ErlenmeyerUser *newUser = [[ErlenmeyerUser alloc] init];
    [newUser setUuid: [[NSUUID UUID] description]];
    [newUser setEmail: @"test@megabitsapp.com"];
    
    ErlenmeyerPost *newPost = [[ErlenmeyerPost alloc] init];
    [newPost setUuid: [[NSUUID UUID] description]];
    [newPost setText: @"This is a new post!"];
    [newPost setAuthor: newUser];
    
    [newPost save];
    
    XCTAssertFalse([newUser hasChanges], @"%s: newUser (%p) has changes: %@", __PRETTY_FUNCTION__, newUser, [newUser changedValuesForCurrentEvent]);
    XCTAssertFalse([newPost hasChanges], @"%s: newPost (%p) has changes: %@", __PRETTY_FUNCTION__, newPost, [newPost changedValuesForCurrentEvent]);
    
    [NSManagedObject deleteAll];
}

- (void)testGroupLocalSaving
{    
    ErlenmeyerUser *newUser = [[ErlenmeyerUser alloc] init];
    [newUser setUuid: [[NSUUID UUID] description]];
    [newUser setEmail: @"test@megabitsapp.com"];
    
    ErlenmeyerGroup *newGroup = [[ErlenmeyerGroup alloc] init];
    [newGroup setUuid: [[NSUUID UUID] description]];
    [newGroup addMembersObject: newUser];
    
    [newGroup save];
    
    XCTAssertFalse([newUser hasChanges], @"%s: newUser (%p) has changes: %@", __PRETTY_FUNCTION__, newUser, [newUser changedValuesForCurrentEvent]);
    XCTAssertFalse([newGroup hasChanges], @"%s: newGroup (%p) has changes: %@", __PRETTY_FUNCTION__, newGroup, [newGroup changedValuesForCurrentEvent]);
    
    [NSManagedObject deleteAll];
}

#pragma mark - Local Database Output
- (void)testUserLocalFetching
{
    ErlenmeyerUser *newUser = [[ErlenmeyerUser alloc] init];
    [newUser setUuid: [[NSUUID UUID] description]];
    [newUser setEmail: @"test@megabitsapp.com"];
    [newUser save];
    
    NSString *newUserUUID = [newUser uuid];
    ErlenmeyerUser *oldUser = newUser;
    newUser = nil;
    newUser = [ErlenmeyerUser get: newUserUUID];
    
    XCTAssertEqualObjects(oldUser, newUser, @"%s: newUser (%p) got changed from original (%p)", __PRETTY_FUNCTION__, newUser, oldUser);
    
    [NSManagedObject deleteAll];
}

- (void)testGroupLocalFetching
{
    ErlenmeyerUser *newUser = [[ErlenmeyerUser alloc] init];
    [newUser setUuid: [[NSUUID UUID] description]];
    [newUser setEmail: @"test@megabitsapp.com"];
    
    ErlenmeyerGroup *newGroup = [[ErlenmeyerGroup alloc] init];
    [newGroup setUuid: [[NSUUID UUID] description]];
    [newGroup addMembersObject: newUser];
    
    [newGroup save];
    newUser = nil;
    newUser = [[newGroup members] anyObject];
    
    XCTAssertNotNil(newUser, @"%s: newUser (%p) not fetched from [newGroup members]", __PRETTY_FUNCTION__, newUser);
    
    [NSManagedObject deleteAll];
}

#pragma mark - Server Input
/*!- (void)testUserServerSaving
{
    ErlenmeyerUser *newUser = [[ErlenmeyerUser alloc] init];
    [newUser setUuid: [[NSUUID UUID] description]];
    [newUser setEmail: @"test@megabitsapp.com"];
    
    [newUser saveToServer: ^(NSError *error)
    {
        XCTAssertNil(error, @"%s: newUser (%p) failed to save to server with error (%p, %@)", __PRETTY_FUNCTION__, newUser, error, error);
    }];
}

- (void)testPostServerSaving
{
    ErlenmeyerUser *newUser = [[ErlenmeyerUser alloc] init];
    [newUser setUuid: [[NSUUID UUID] description]];
    [newUser setEmail: @"test@megabitsapp.com"];
    
    ErlenmeyerPost *newPost = [[ErlenmeyerPost alloc] init];
    [newPost setUuid: [[NSUUID UUID] description]];
    [newPost setText: @"This is a new post!"];
    [newPost setAuthor: newUser];
    
    [newPost saveToServer: ^(NSError *error)
    {
        XCTAssertNil(error, @"%s: newPost (%p) failed to save to server with error (%p, %@)", __PRETTY_FUNCTION__, newPost, error, error);
    }];
}*/

#pragma mark - Local Model Copying
- (void)testModelCopying
{
    ErlenmeyerUser *newUser = [[ErlenmeyerUser alloc] init];
    [newUser setUuid: [[NSUUID UUID] description]];
    [newUser setEmail: @"test@megabitsapp.com"];
    
    ErlenmeyerPost *newPost = [[ErlenmeyerPost alloc] init];
    [newPost setUuid: [[NSUUID UUID] description]];
    [newPost setText: @"This is a new post!"];
    [newPost setAuthor: newUser];
    
    ErlenmeyerGroup *newGroup = [[ErlenmeyerGroup alloc] init];
    [newGroup setUuid: [[NSUUID UUID] description]];
    [newGroup addMembersObject: newUser];
    
    // Deep copy of group
    ErlenmeyerGroup *copiedGroup = [newGroup copyToKeyPaths: @[@"members", @"members.posts"]];
    ErlenmeyerUser *copiedUser = [[copiedGroup members] anyObject];
    ErlenmeyerPost *copiedPost = [[copiedUser posts] anyObject];
    
    XCTAssertFalse(copiedGroup == newGroup, @"%s: copiedGroup (%p) == newGroup (%p)", __PRETTY_FUNCTION__, copiedGroup, newGroup);
    
    XCTAssertFalse(copiedUser == newUser, @"%s: copiedUser (%p) == newUser (%p)", __PRETTY_FUNCTION__, copiedUser, newUser);
    XCTAssertEqualObjects([copiedUser uuid], [newUser uuid], @"%s: [copiedUser uuid] (%p) does not equal [newUser uuid] (%p)", __PRETTY_FUNCTION__, [copiedUser uuid], [newUser uuid]);
    XCTAssertEqualObjects([copiedUser email], [newUser email], @"%s: [copiedUser email] (%p) does not equal [newUser email] (%p)", __PRETTY_FUNCTION__, [copiedUser email], [newUser email]);
    
    XCTAssertFalse(copiedPost == newPost, @"%s: copiedPost (%p) == newPost (%p)", __PRETTY_FUNCTION__, copiedPost, newPost);
    XCTAssertEqualObjects([copiedPost uuid], [newPost uuid], @"%s: [copiedPost uuid] (%p) does not equal [newPost uuid] (%p)", __PRETTY_FUNCTION__, [copiedPost uuid], [newPost uuid]);
    XCTAssertEqualObjects([copiedPost text], [newPost text], @"%s: [copiedPost text] (%p) does not equal [newPost text] (%p)", __PRETTY_FUNCTION__, [copiedPost text], [newPost text]);
}



@end
