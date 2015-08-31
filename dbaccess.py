import psycopg2

class PostgreSQL(object):
    def __init__(self, db_name):
        "docstring"
        self.db = db_name
        self.conn_str = "dbname={0} user=postgres".format(db_name)

    def _connect(self):
        return psycopg2.connect(self.conn_str)

    def get_column_names(self,table_name):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("select column_name, data_type from information_schema.columns  where table_name = (%s)",(table_name,))
        return cursor
        
    def get_table_names(self):
        with  self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("select table_name from information_schema.tables where table_schema='public'") 
        return cursor
