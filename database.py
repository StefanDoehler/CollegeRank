import MySQLdb
import common


def connect_db():
    try:
        db = MySQLdb.connect(host=common.host,
                             user=common.user,
                             passwd=common.password,
                             db=common.db_name)
        return db
    except MySQLdb.Error as e:
        print e
        return False


def create_schema():
    connection = connect_db()

    if connection is False:
        print "Database cannot be accessed at this time"
        return

    cursor = connection.cursor()
    tables = {}
    tables["Scores"] = (
        """CREATE TABLE Scores(
        score_ID int(11) NOT NULL AUTO_INCREMENT,
        rank int(11),
        average int(11),
        num_lists int(11),
        PRIMARY KEY (score_ID))
        ENGINE=InnoDB"""
    )
    tables["Locations"] = (
        """CREATE TABLE Locations(
        location_ID int(11) NOT NULL AUTO_INCREMENT,
        city varchar(40),
        state varchar(15),
        region varchar(10),
        PRIMARY KEY (location_ID))
        ENGINE=InnoDB"""
    )
    tables["Schools"] = (
        """CREATE TABLE Schools(
        name varchar(50) NOT NULL,
        score int(11),
        location int(11),
        PRIMARY KEY (name),
        FOREIGN KEY (score) REFERENCES Scores(score_ID),
        FOREIGN KEY (location) REFERENCES Locations(location_ID))
        ENGINE=InnoDB"""
    )

    for name, schema in tables.iteritems():
        try:
            cursor.execute(schema)
            connection.commit()
        except MySQLdb.Error as e:
            print e

    cursor.close()
    connection.close()





