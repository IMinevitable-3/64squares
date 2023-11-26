import os

SECRET_KEY = os.environ.get('SECRET_KEY' , 'nothing')
DJANGO_DEBUG = os.environ.get('DEBUG' , True) 

DATABASE_URL = os.environ.get('DATABASE_URL', '127.0.0.1')
DATABASE_NAME = os.environ.get('DATABASE_NAME', 'mydb')
DATABASE_USER = os.environ.get('DATABASE_USER', 'root')
DATABASE_PASS = os.environ.get('DATABASE_PASS', '123')
DATABASE_PORT = os.environ.get('DATABASE_PORT', '5432')

REDIS_URL = os.environ.get('REDIS_URL' , 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT' , '6379')