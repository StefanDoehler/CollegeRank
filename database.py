import MySQLdb


def connect_db():
    try:
        db = MySQLdb.connect(host="localhost",
                             user="Stefan",
                             passwd="cpsc437",
                             db="CollegeRankDB")
    except MySQLdb.Error as e:
        print e

connect_db()
