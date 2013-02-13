//
//  NSManagedObject_ErlenmeyerTestsDetailViewController.m
//  NSManagedObject_ErlenmeyerTests
//
//  Created by Patrick Perini on 2/13/13.
//  Copyright (c) 2013 MegaBits. All rights reserved.
//

#import "NSManagedObject_ErlenmeyerTestsDetailViewController.h"

@interface NSManagedObject_ErlenmeyerTestsDetailViewController ()
- (void)configureView;
@end

@implementation NSManagedObject_ErlenmeyerTestsDetailViewController

#pragma mark - Managing the detail item

- (void)setDetailItem:(id)newDetailItem
{
    if (_detailItem != newDetailItem) {
        _detailItem = newDetailItem;
        
        // Update the view.
        [self configureView];
    }
}

- (void)configureView
{
    // Update the user interface for the detail item.

    if (self.detailItem) {
        self.detailDescriptionLabel.text = [[self.detailItem valueForKey:@"timeStamp"] description];
    }
}

- (void)viewDidLoad
{
    [super viewDidLoad];
	// Do any additional setup after loading the view, typically from a nib.
    [self configureView];
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        self.title = NSLocalizedString(@"Detail", @"Detail");
    }
    return self;
}
							
@end
