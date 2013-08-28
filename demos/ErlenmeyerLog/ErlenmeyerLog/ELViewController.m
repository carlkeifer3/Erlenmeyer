//
//  ELViewController.m
//  ErlenmeyerLog
//
//  Created by Patrick Perini on 8/26/13.
//  Copyright (c) 2013 pcperini. All rights reserved.
//

#import "ELViewController.h"
#import "ELUser.h"
#import "ELUser+ELExtensions.h"
#import "ELMessage.h"
#import "NSManagedObject+EKManagedObjectExtensions.h"
#import "NSManagedObject+EKQueryingExtensions.h"

#define kUsernameKey @"username"
#define kCellReuseID @"cellresuseid"

@implementation ELViewController

- (void)viewDidLoad
{
    [super viewDidLoad];
    [NSManagedObject setServerURL: @"http://localhost:8080"];
    
    if (![self user])
    {
        NSString *username = [[NSUserDefaults standardUserDefaults] stringForKey: kUsernameKey];
        if (!username)
        {
            __weak typeof(self) weakself = self;
            UIAlertView *alertView = [[UIAlertView alloc] initWithTitle: @"Username?"
                                                                message: nil
                                                               delegate: weakself
                                                      cancelButtonTitle: nil
                                                      otherButtonTitles: @"OK", nil];
            
            [alertView setAlertViewStyle: UIAlertViewStylePlainTextInput];
            [alertView show];
        }
        else
        {
            [self setUser: [ELUser userWithUsername: username]];
        }
    }
}

- (void)setUser:(ELUser *)user
{
    _user = user;
    [[NSUserDefaults standardUserDefaults] setObject: [user username]
                                              forKey: kUsernameKey];
    [[NSUserDefaults standardUserDefaults] synchronize];
    [NSManagedObject saveAll];
}

- (BOOL)alertViewShouldEnableFirstOtherButton:(UIAlertView *)alertView
{
    return [[alertView textFieldAtIndex: 0] text] && ![[[alertView textFieldAtIndex: 0] text] isEqualToString: @""];
}

- (void)alertView:(UIAlertView *)alertView didDismissWithButtonIndex:(NSInteger)buttonIndex
{
    NSString *username = [[alertView textFieldAtIndex: 0] text];

//    // --------------
//    [self setUser: [ELUser userWithUsername: username]];
//    // --------------
    
      [ELUser allFromServer: ^(NSArray *all, NSError *error)
      {
          if (error || [all count] <= 0)
          {
              [self setUser: [ELUser userWithUsername: username]];
              [[self user] saveToServer: ^(NSError *error)
               {
                   [NSManagedObject saveAll];
                   [[self tableView] reloadData];
               }];
              
              return;
          }
          
          [self setUser: [all firstObject]];
          [ELMessage allFromServer: ^(NSArray *all, NSError *error)
           {
               [NSManagedObject saveAll];
               [[self tableView] reloadData];
           } where: @{@"_author_uuid": [[self user] uuid]}];
      } where: @{@"username": username}];
}

- (BOOL)textFieldShouldReturn:(UITextField *)textField
{
    ELMessage *newMessage = [[ELMessage alloc] init];
    [newMessage setUuid: [[NSUUID UUID] UUIDString]];
    [newMessage setText: [textField text]];
    [newMessage setAuthor: [self user]];
    [newMessage setTimestamp: @([[NSDate date] timeIntervalSince1970])];
    
//    // --------------
//    [NSManagedObject saveAll];
//    
//    [textField setText: @""];
//    [textField resignFirstResponder];
//    
//    [[self tableView] reloadData];
//    // --------------
    
    [newMessage saveToServer: ^(NSError *error)
    {
        if (error)
            return;
        
        [NSManagedObject saveAll];
        
        [textField setText: @""];
        [textField resignFirstResponder];
        
        [ELMessage allFromServer: ^(NSArray *all, NSError *error)
        {
            [NSManagedObject saveAll];
            [[self tableView] reloadData];
        } where: @{}];
    }];
    
    return YES;
}

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView
{
    return 1;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section
{
    if (![self user])
        return 0;
    
    return [[[self user] messages] count];
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath
{
    ELMessage *message = [[[self user] messagesInChronologicalOrder] objectAtIndex: [indexPath row]];
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier: kCellReuseID];
    if (!cell)
    {
        cell = [[UITableViewCell alloc] initWithStyle: UITableViewCellStyleSubtitle
                                      reuseIdentifier: kCellReuseID];
    }
    
    [[cell textLabel] setText: [message text]];
    [[cell detailTextLabel] setText: [NSString stringWithFormat: @"%@ at %@",
        [[message author] username],
        [NSDate dateWithTimeIntervalSince1970: [[message timestamp] integerValue]]
    ]];
    
    return cell;
}

@end
