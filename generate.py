from dbmodels import dbModel
from modelgenerator import *
import sys, argparse

def generate(db_type, db_name, db_user, dest):
    p = dbModel.map_db_accessor(db_type, db_name, db_user)
    for table in p.get_table_names():
        print(table)
        pk = p.get_primary_key(table)
        cols = { n:None for n,_ in p.get_column_names(table)}
        m = ModelGenerator()
        m.generate(primary_key = pk,
                   vars = cols,
                   defs = {'__init__':{'args':'','body':''}},
                   class_name = table + '_model',
                   imports={},
                   dest = dest)
        print(m.generated)

        r = ModelGenerator()
        rimports = {m.class_name:'*'}
        rimports.update(p.imports)

        r.generate(primary_key = pk,
                   imports=rimports,
                   vars = {'model':m.class_name+'()'},
                   defs = {'__init__':{'args':'',
                                       'body':''},
                           'connect':{'args':'',
                                      'body': p.gen_conn_string_body()},
                           'select':{'args':pk,
                                     'body':p.gen_select_query(table, pk)},
                           'insert':{'args':m.class_name,
                                     'body':p.gen_insert_query(table, m.class_name)}
                           },
                   class_name = table + '_repository',
                   dest = dest)
        print(r.generated)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--db_type", help="Type of databse, valid values are: psql,", required=True)
    parser.add_argument("-db","--db_name", help="The name of the database", required=True)
    parser.add_argument("-u","--db_user", help="The user name of the database", required=True)
    parser.add_argument("-dst","--dest", help="The destination folder to write the generated models to", required=False, default='models')
    args = parser.parse_args()
    generate(args.db_type, args.db_name, args.db_user, args.dest)
    
if __name__ == "__main__":
    main(sys.argv)
