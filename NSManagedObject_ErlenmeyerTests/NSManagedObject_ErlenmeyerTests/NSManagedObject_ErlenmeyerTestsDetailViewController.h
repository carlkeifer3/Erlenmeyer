//
//  NSManagedObject_ErlenmeyerTestsDetailViewController.h
//  NSManagedObject_ErlenmeyerTests
//
//  Created by Patrick Perini on 2/13/13.
//  Copyright (c) 2013 MegaBits. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface NSManagedObject_ErlenmeyerTestsDetailViewController : UIViewController

@property (strong, nonatomic) id detailItem;

@property (weak, nonatomic) IBOutlet UILabel *detailDescriptionLabel;
@end
