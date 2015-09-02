import psycopg2

class PostgreSQL(object):
    def __init__(self, db_name, db_user):
        self.db = db_name
        self.conn_str = "dbname={0} user= {1}".format(db_name, db_user)
        self.imports ={'psycopg2':''}

    def _connect(self):
        return psycopg2.connect(self.conn_str)

    def gen_conn_string_body(self):
        body ="\t\treturn psycopg2.connect('{0}')\n".format(self.conn_str)
        return body

    def gen_query_body(self, query, qargs):
        body = "\t\twith self.connect() as conn:\n"
        body += "\t\t\tcursor = conn.cursor()\n"
        body += """\t\t\tcursor.execute("{0}", ({1},))\n""".format(query,qargs)
        body += "\t\t\treturn cursor\n"
        return body
        
    def get_column_names(self,table_name):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("select column_name, data_type from information_schema.columns  where table_name = (%s)",(table_name,))
            return cursor
        
    def get_table_names(self):
        with  self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("select table_name from information_schema.tables where table_schema='public'")
            return [row[0] for row in cursor]

    def get_primary_key(self, table_name):
        with  self._connect() as conn:
            cursor = conn.cursor()
            query ='''SELECT 
                 columns.column_name
               FROM 
                 information_schema.columns, 
                 information_schema.table_constraints, 
                 information_schema.constraint_column_usage
               WHERE 
                 columns.column_name = constraint_column_usage.column_name AND
                 constraint_column_usage.constraint_name = table_constraints.constraint_name AND
                 table_constraints.constraint_type = 'PRIMARY KEY' AND 
                 columns.table_name = (%s) ;'''
            cursor.execute(query,(table_name,))
            row = cursor.fetchone()
            if row == None:
                return ''
            return row[0]
        
