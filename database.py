import MySQLdb
import common


def connect_db():
    try:
        db_connection = MySQLdb.connect(host=common.host,
                                        user=common.user,
                                        passwd=common.password,
                                        db=common.db_name)
        return db_connection
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


def add_school(school_name, school_info, connection, cursor):
    if school_name is None or school_info is None or school_info[0] is None:  # if data corrupted, don't add to database
        return

    location, count, average_rank = school_info[0], school_info[1], school_info[2]
    city = location[0]
    state = location[1]
    region = location[2]

    location_sql = """
        INSERT INTO Locations (city, state, region)
         VALUES (%s, %s, %s)
    """
    score_sql = """
        INSERT INTO Scores (average, num_lists)
         VALUES (%s, %s)
    """
    school_sql = """
        INSERT INTO Schools (name, score, location)
         VALUES (%s, %s, %s)
    """

    cursor.execute(location_sql, (city, state, region))
    location_fk = cursor.lastrowid                       # get the location foreign key
    cursor.execute(score_sql, (average_rank, count))
    score_fk = cursor.lastrowid                          # get the score foreign key
    cursor.execute(school_sql, (school_name, score_fk, location_fk))
    connection.commit()

#create_schema()
#cursor = con.cursor()
#add_school("Yale University", [["New Haven", "Connecticut", "Northeast"], 5, 16], con, cursor)
#add_school("USF", [["San Francisco", "California", "West"], 2, 33], con, cursor)
#cursor.close()
#con.close()
