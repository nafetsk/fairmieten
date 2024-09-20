from .defaults import *
from .logging import *
from .mods import *


"""
if you need to include a setting file from another app you could use some like this:
******* 
try:
	from tail.settings import *
except ImportError or ModuleNotFoundError:
    print('No Module settings in tails')
*******
"""

# STATIC_ROOT = 'staticfiles/'
