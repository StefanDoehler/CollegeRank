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


def create_db():
    db = MySQLdb.connect(host="127.0.0.1",
                         port=3306,
                         user=common.user,
                         passwd=common.password)
    cursor = db.cursor()
    sql = "CREATE DATABASE CollegeRank"

create_db()

