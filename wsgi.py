# WSGI file for PythonAnywhere deployment
import sys
import os

# Add your project directory to sys.path
path = '/home/yourusername/mysite'  # Replace 'yourusername' with your actual username
if path not in sys.path:
    sys.path.insert(0, path)

from app import app as application

if __name__ == "__main__":
    application.run()
