"""
"""

import os

try:
    _env_type = os.environ['CHOPSTIX_ENVIRONMENT_TYPE']
except KeyError:
    from local import *
else:
    if _env_type == 'PRODUCTION':
        from production import *
