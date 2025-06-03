import sys
import os

# Adjust this path to match your actual username and directory
project_home = '/home/smartpotato86/CHAT-APP'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from webapp import app as application  # the `app` is defined in __init__.py
