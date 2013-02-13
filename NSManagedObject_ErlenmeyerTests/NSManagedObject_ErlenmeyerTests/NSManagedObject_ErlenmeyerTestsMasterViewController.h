//
//  NSManagedObject_ErlenmeyerTestsMasterViewController.h
//  NSManagedObject_ErlenmeyerTests
//
//  Created by Patrick Perini on 2/13/13.
//  Copyright (c) 2013 MegaBits. All rights reserved.
//

#import <UIKit/UIKit.h>

@class NSManagedObject_ErlenmeyerTestsDetailViewController;

#import <CoreData/CoreData.h>

@interface NSManagedObject_ErlenmeyerTestsMasterViewController : UITableViewController <NSFetchedResultsControllerDelegate>

@property (strong, nonatomic) NSManagedObject_ErlenmeyerTestsDetailViewController *detailViewController;

@property (strong, nonatomic) NSFetchedResultsController *fetchedResultsController;
@property (strong, nonatomic) NSManagedObjectContext *managedObjectContext;

@end
