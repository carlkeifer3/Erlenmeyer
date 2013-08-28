//
//  ELViewController.h
//  ErlenmeyerLog
//
//  Created by Patrick Perini on 8/26/13.
//  Copyright (c) 2013 pcperini. All rights reserved.
//

#import <UIKit/UIKit.h>
@class ELUser;

@interface ELViewController : UIViewController <UITextFieldDelegate, UIAlertViewDelegate, UITableViewDataSource, UITableViewDelegate>

@property (nonatomic) ELUser *user;
@property IBOutlet UITableView *tableView;

@end
