from os import environ
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

BASIC_AUTHORIZATION_HEADER_VALUE = environ.get('BASIC_AUTHORIZATION_HEADER_VALUE')
X_AUTH_TOKEN_HEADER_VALUE = environ.get('X_AUTH_TOKEN_HEADER_VALUE')
