import MySQLdb
import common


def connect_db():
    try:
        db = MySQLdb.connect(host=common.host,
                             user=common.user,
                             passwd=common.password,
                             db=common.db_name)
        return db.cursor()
    except MySQLdb.Error as e:
        print e
        return False


def create_schema():
    cursor = connect_db()

    if cursor is False:
        print "Database cannot be accessed at this time"
        return

    school_table_sql = ""
    cursor.close()

create_schema()