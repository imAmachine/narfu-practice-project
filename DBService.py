import psycopg2


class DBService:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.connection.connection.close()

    def exec_query(self, query):
        """
        Method executing a SELECT query

        :param query: SQL query to execute
        :return: list of query results
        """
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except psycopg2.DatabaseError as e:
            self.connection.rollback()
            raise e
        finally:
            self.cursor.close()

    def exec_select(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except psycopg2.DatabaseError as e:
            self.connection.rollback()
            raise e
        finally:
            self.cursor.close()
