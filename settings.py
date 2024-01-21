import os
from os.path import join, dirname
from dotenv import load_dotenv

# Load .env file
dotenv_path = join(dirname(__file__), 'vars.env')
load_dotenv(dotenv_path)

# Facebook OAuth
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')


