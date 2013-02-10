#
#  __init__.py
#  Erlenmeyer
#
#  Created by Patrick Perini on February 3, 2013.
#  See LICENSE.txt for licensing information.
#

class category(object):
    def __init__(self, destination, override = True):
        self.destination = destination
        self.override = override
        
    def __call__(self, function):
        if self.override or function.__name__ not in dir(self.destionation):
            setattr(self.destination, function.__name__, function)
            
def categorize(destination, function, override = True):
    category(destination, override).__call__(function)

def addCategories(destination, source, override = True, list = None):
    if not list:
        list = dir(module)
        
    for function in list:
        try:
            categorize(destination, getattr(source, function), override)
        except AttributeError:
            pass
            
