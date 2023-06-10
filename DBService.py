import psycopg2


class DBService:
    def __init__(self, db, username, password, host, port):
        self.db = db
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cur = None

    def service_init(self, schema):
        self.conn = psycopg2.connect(dbname=self.db, user=self.username, password=self.password,
                                     host=self.host, port=self.port)
        self.cur = self.conn.cursor()

    def exec_select(self, obj, cols):
        """
            Method executing SELECT query from an object representing a database table

            :param obj: database table object
            :param cols: param representing columns to selecting from a table
            :return: list of table rows
        """
        return self.cur.execute(obj.get_sql_select(cols))
