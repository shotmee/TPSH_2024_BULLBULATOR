import os

_basedir = os.path.abspath(os.path.dirname(__file__))

ADMINS = frozenset(['dmaswinf@yandex.ru'])
SECRET_KEY = 'afdwEF2Q34XRQ43CRQ324CXF24FQEW'

SQLALCHEMY_DATABASE_URI = 'sqlite:///dbase.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}