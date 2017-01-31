from os import environ

BASIC_AUTHORIZATION_HEADER_VALUE = environ.get('BASIC_AUTHORIZATION_HEADER_VALUE')
X_AUTH_TOKEN_HEADER_VALUE = environ.get('X_AUTH_TOKEN_HEADER_VALUE')
SECRET_KEY = environ.get('SECRET_KEY')
ENGINE = environ.get('ENGINE')
NAME = environ.get('NAME')
USER = environ.get('USER')
PASSWORD = environ.get('PASSWORD')
HOST = environ.get('HOST')
PORT = environ.get('PORT')