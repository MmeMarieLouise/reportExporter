import os
basedir = os.path.abspath(os.path.dirname(__file__))

# config class for entire flask project
class Config(object):
    # environment variable
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # this always must be defined with database url/ connection string passed into variable
    SQLALCHEMY_DATABASE_URI = 'postgresql://interview:uo4uu3AeF3@candidate.suade.org/suade'