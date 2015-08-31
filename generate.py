from dbmodels import dbModel
from modelgenerator import ModelGenerator
import sys, argparse

def generate(db_type, db_name, db_user, dest):
    p = dbModel.map_db_accessor(db_type, db_name, db_user)
    for x in p.get_table_names():
        m = ModelGenerator()
        m.gen_class_string(x[0])
        m.gen_def_string('__init__')
        for n,t in p.get_column_names(x[0]):
                m.gen_self_var(n)
        m.write_to_file(dest)
        print("Generated:",m.class_name)

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
