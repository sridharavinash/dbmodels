from dbaccess import *

class dbModel(object):
    @staticmethod
    def map_db_accessor(db_type, db_name, db_user):
        if(db_type == 'psql'):
            return PostgreSQL(db_name, db_user)
        return None
