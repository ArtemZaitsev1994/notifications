import os


SECRET_KEY =  os.environ.get('SECRET_KEY', 'foo')

NEW_CHATS_PER_DAY_LIMIT = 15

POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'postgres')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', 5432)
DATABASE = os.environ.get('DATABASE', 'notifications')
DATABASE_NAME = os.environ.get('DATABASE_NAME', 'notifications')

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)

MONOLITH_HOST = os.environ.get('MONOLITH_HOST', 'http://127.0.0.1')
MONOLITH_PORT = os.environ.get('MONOLITH_PORT', '8000')

MAIN_SERVER_URL = f'{MONOLITH_HOST}:{MONOLITH_PORT}'

RABBIT_HOST = os.environ.get('RABBIT_HOST', 'amqp://guest:guest@localhost/')
RABBIT_WEBSOCKETS_EXCHANGE = 'websockets_notifications'
RABBIT_NOTIFICATIONS_EXCHANGE = 'notifications'


SECRET_KEY = os.environ.get('SECRET_KEY', 'foo')