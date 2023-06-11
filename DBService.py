import psycopg2


class DBService:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = None

    def service_init(self, schema):
        self.cursor = self.connection.cursor(schema)

    def close_connection(self):
        self.connection.connection.close()

    def exec_select(self, query):
        """
        Method executing a SELECT query

        :param query: SQL query to execute
        :return: list of query results
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def exec_call(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            cursor.callproc(query, params)
            self.connection.commit()
        except psycopg2.DatabaseError as e:
            self.connection.rollback()
            raise e
        finally:
            cursor.close()
