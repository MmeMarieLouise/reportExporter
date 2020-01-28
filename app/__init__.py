from flask import Flask, g
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)


from app import routes

@app.before_request
def create_postgres_conn():
    engine = create_engine('postgresql+psycopg2://interview:uo4uu3AeF3@candidate.suade.org/suade')
    g.conn = engine.connect()


