"""
core/settings/__init__.py

Import the correct settings based on DJANGO_ENV environment variable.
Defaults to development if not set.
"""

import os

env = os.environ.get("DJANGO_ENV", "development")

if env == "production":
    from .production import *
elif env == "staging":
    from .staging import *
else:
    from .development import *
