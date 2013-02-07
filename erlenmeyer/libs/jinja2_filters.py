#
#  jinja2_filters.py
#  Erlenmeyer
#
#  Created by Patrick Perini on February 6, 2013.
#  See LICENSE.txt for licensing information.
#

def camelcase(value):
    value = list(value)
    value[0] = value[0].upper()
    value = ''.join(value)
    return value