import psycopg2
import psycopg2.extras

from psycopg2.pool import ThreadedConnectionPool
from singleton_decorator import singleton


# Write wrapper on postgres library to get multi thread connection and stop database leaking written by wakeel
# Multi-threaded & Singleton wrapper to the postgres driver
@singleton
class PgPool:
    def __init__(self):
        self.host, self.port = None, None
        self.database, self.pool = None, None
        self.user, self.passwd = None, None
        self.pool = None

    def create_pool(self, conn_dict):
        """
        Create a connection pool

        :param conn_dict: connection params dictionary
        :type conn_dict: dict
        """
        if conn_dict["Host"] is None:
            self.host = 'localhost'
        else:
            self.host = conn_dict["Host"]
        if conn_dict["Port"] is None:
            self.port = '5432'
        else:
            self.port = conn_dict["Port"]

        self.database = conn_dict["Database"]
        self.user = conn_dict["User"]
        self.passwd = conn_dict["Password"]

        conn_params = "host='{host}' dbname='{db}' user='{user}' password='{passwd}' port='{port}'".format(
            host=self.host, db=self.database, user=self.user, passwd=self.passwd, port=self.port
        )

        try:
            self.pool = ThreadedConnectionPool(1, 50, conn_params)
        except Exception as e:
            print(e.message)

    def get_conn(self):
        """
        Get a connection from pool and return connection and cursor
        :return: conn, cursor
        """
        try:
            conn = self.pool.getconn()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            return conn, cursor
        except Exception as e:
            print(e.message)
            return None, None

    @staticmethod
    def execute_query(cursor, query, params):
        """
        Execute a query on database

        :param cursor: cursor object
        :param query: database query
        :type query: str
        :param params: query parameters
        :type params: tuple
        :return: query results or bool
        """

        try:
            if query.split()[0].lower() == 'select':
                cursor.execute(query, params)
                return cursor.fetchall()
            else:
                return cursor.execute(query, params)
        except Exception as e:
            print(e.message)
            return False

    # commit changes to db permanently
    @staticmethod
    def commit_changes(conn):
        """
        Commit changes to the database permanently

        :param conn: connection object
        :return: bool
        """
        try:
            return conn.commit()
        except Exception as e:
            print(e.message)
            return False

    def put_conn(self, conn):
        """
        Put connection back to the pool

        :param conn: connection object
        :return: bool
        """
        try:
            return self.pool.putconn(conn)
        except Exception as e:
            print(e.message)
            return False

    def close_pool(self):
        """
        Closes connection pool
        :return: bool
        """
        try:
            return self.pool.closeall()
        except Exception as e:
            print(e.message)
            return False
