import ConfigParser

from app import app
from app.common.db.postgres import PgPool

app.config.from_object('config.DevelopmentConfig')

config = ConfigParser.ConfigParser()
config.read("../config.ini")

db_conn_params = {
    "Host": config.get('Database', 'Host'),
    "Port": config.get('Database', 'Port'),
    "Database": config.get('Database', 'Database'),
    "User": config.get('Database', 'User'),
    "Password": config.get('Database', 'Password')
}

db_conn = PgPool()
db_conn.create_pool(db_conn_params)

app.run(host='0.0.0.0', port=9000)
