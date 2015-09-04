import psycopg2
import inspect

class PostgreSQL(object):
    def __init__(self, db_name, db_user):
        self.db = db_name
        self.conn_str = "dbname={0} user= {1}".format(db_name, db_user)
        self.imports ={'psycopg2':''}

    def _connect(self):
        return psycopg2.connect(self.conn_str)

    def gen_select_query(self,table,pk):
        q = "SELECT * FROM {0} WHERE {1} = (%s)".format(table,pk)
        return self.gen_query_body(q,pk)

    def gen_insert_query(self,table, model_name):
        body = "\t\twith self.connect() as conn:\n"
        body+= "\t\t\targs_tuple = [(z,{0}.__dict__[z],type({0}.__dict__[z]).__name__) for z in {0}.__dict__ if not z.startswith('__')]\n".format(model_name)
        body += """\t\t\tcargs = []\n"""
        body += """\t\t\tvargs = []\n"""
        body += "\t\t\tfor col,val,t in args_tuple:\n"
        body +="\t\t\t\tcargs.append(col)\n"
        body += "\t\t\t\tif(t == 'str'):\n"
        body += "\t\t\t\t\tvargs.append('{0}'.format(val))\n"
        body +="\t\t\t\telse:\n"
        body += "\t\t\t\t\tvargs.append(val)\n"
        body += "\t\t\tcursor = conn.cursor()\n"
        body += """\t\t\tcursor.execute("INSERT INTO {0} {1} VALUES {2}".format(cargs,vargs,))\n""".format(table, '{0}', '{1}')
        body += "\t\t\treturn cursor\n"
        return body

    
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
        
