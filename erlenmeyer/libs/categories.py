#
#  __init__.py
#  Erlenmeyer
#
#  Created by Patrick Perini on February 3, 2013.
#  See LICENSE.txt for licensing information.
#

class category(object):
    def __init__(self, mainModule, override = True):
        self.mainModule = mainModule
        self.override = override
        
    def __call__(self, function):
        if self.override or function.__name__ not in dir(self.mainModule):
            setattr(self.mainModule, function.__name__, function)
            
    def categorize(module, function, override = True):
        category(module, override).__call__(function)
    
    def addCategories(mainModule, module, override = True):
        for function in dir(module):
            categorize(mainModule, getattr(module, function), override)