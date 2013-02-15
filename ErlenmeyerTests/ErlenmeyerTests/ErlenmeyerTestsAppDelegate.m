//
//  ErlenmeyerTestsAppDelegate.m
//  ErlenmeyerTests
//
//  Created by Patrick Perini on 2/13/13.
//  Copyright (c) 2013 MegaBits. All rights reserved.
//

#import <CoreData/CoreData.h>
#import "ErlenmeyerTestsAppDelegate.h"
#import "ErlenmeyerTestsViewController.h"
#import "NSManagedObject+ErlenmeyerExtensions.h"
#import "ErlenmeyerModel.h"
#import "ErlenmeyerGroup.h"
#import "ErlenmeyerPost.h"
#import "ErlenmeyerUser.h"

@implementation ErlenmeyerTestsAppDelegate

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions
{
    self.window = [[UIWindow alloc] initWithFrame:[[UIScreen mainScreen] bounds]];
    // Override point for customization after application launch.
    self.viewController = [[ErlenmeyerTestsViewController alloc] initWithNibName:@"ErlenmeyerTestsViewController" bundle:nil];
    self.window.rootViewController = self.viewController;
    [self.window makeKeyAndVisible];
    
    [NSManagedObject initializeObjects];
    [NSManagedObject setServerURL: @"http://einstein.pcperini.com:8080"];
//    ErlenmeyerUser *user = [[ErlenmeyerUser alloc] init];
//    [user setUuid: @"0001"];
//    [user save];
//    ErlenmeyerGroup *group = [[ErlenmeyerGroup alloc] init];
//    [group setUuid: @"0002"];
//    
//    ErlenmeyerUser *user = [ErlenmeyerUser get: @"0001"];
//    [group addMembersObject: user];
//    [group save];
    
//    ErlenmeyerUser *user = [ErlenmeyerUser get: @"0001"];
//    [user saveToServer: ^(NSError *error) {
//        NSLog(@"%@", error);        
//    }];

//    [ErlenmeyerUser allFromServer: ^(NSArray *all, NSError *error) {
//        NSLog(@"%@, %@", all, error);
//    }];
    
    [ErlenmeyerUser allFromServer: ^(NSArray *all, NSError *error) {
        NSLog(@"%@", all);
    }];
    
    return YES;
}

- (void)applicationWillResignActive:(UIApplication *)application
{
    // Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
    // Use this method to pause ongoing tasks, disable timers, and throttle down OpenGL ES frame rates. Games should use this method to pause the game.
}

- (void)applicationDidEnterBackground:(UIApplication *)application
{
    // Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later. 
    // If your application supports background execution, this method is called instead of applicationWillTerminate: when the user quits.
}

- (void)applicationWillEnterForeground:(UIApplication *)application
{
    // Called as part of the transition from the background to the inactive state; here you can undo many of the changes made on entering the background.
}

- (void)applicationDidBecomeActive:(UIApplication *)application
{
    // Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
}

- (void)applicationWillTerminate:(UIApplication *)application
{
    // Called when the application is about to terminate. Save data if appropriate. See also applicationDidEnterBackground:.
}

@end
