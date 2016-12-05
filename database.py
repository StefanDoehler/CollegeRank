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
    create_scores = (
        """CREATE TABLE Scores(
        score_ID int(11) NOT NULL AUTO_INCREMENT,
        average float(11),
        num_lists int(11),
        PRIMARY KEY (score_ID))
        ENGINE=InnoDB"""
    )
    create_locations = (
        """CREATE TABLE Locations(
        location_ID int(11) NOT NULL AUTO_INCREMENT,
        city varchar(40),
        state varchar(25),
        region varchar(15),
        PRIMARY KEY (location_ID))
        ENGINE=InnoDB"""
    )
    create_schools = (
        """CREATE TABLE Schools(
        name varchar(50) NOT NULL,
        score int(11),
        location int(11),
        PRIMARY KEY (name),
        FOREIGN KEY (score) REFERENCES Scores(score_ID),
        FOREIGN KEY (location) REFERENCES Locations(location_ID))
        ENGINE=InnoDB"""
    )

    try:
        cursor.execute(create_scores)
        cursor.execute(create_locations)
        cursor.execute(create_schools)
        connection.commit()
    except MySQLdb.Error as e:
        print e

    cursor.close()
    connection.close()


def add_school(school_name, school_info, connection, cursor):
    if school_name is None or school_info is None or not school_info[0]:  # if data corrupted, don't add to database
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
    try:
        cursor.execute(school_sql, (school_name, score_fk, location_fk))
    except MySQLdb.Error as e:
        print e
    connection.commit()


def delete_tables():
    connection = connect_db()

    if connection is False:
        print "Database cannot be accessed at this time"
        return

    cursor = connection.cursor()
    try:
        cursor.execute("DROP TABLE Schools")
        cursor.execute("DROP TABLE Scores")
        cursor.execute("DROP TABLE Locations")
    except MySQLdb.Error as e:
        print e

    cursor.close()
    connection.close()


def query_all_schools(limit):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT a.name, b.average, c.city, c.state, c.region FROM Schools AS a
         INNER JOIN Scores AS b ON a.score = b.score_ID
          INNER JOIN Locations AS c ON a.location = c.location_ID
           ORDER BY b.average
            LIMIT %s
    """, limit)
    result = cursor.fetchall()
    cursor.close()
    connection.close()

    return result


def query_by_state(state, limit):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT a.name, b.average, c.city, c.state, c.region FROM schools AS a
         INNER JOIN Scores AS b ON a.score = b.score_ID
          INNER JOIN (SELECT * FROM Locations AS c WHERE state = %s) AS c ON a.location = c.location_ID
           ORDER BY b.average
            LIMIT %s
    """, (state, limit))
    result = cursor.fetchall()
    cursor.close()
    connection.close()

    return result


def query_by_region(region, limit):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT a.name, b.average, c.city, c.state, c.region FROM schools AS a
         INNER JOIN Scores AS b ON a.score = b.score_ID
          INNER JOIN (SELECT * FROM Locations AS c WHERE region = %s) AS c ON a.location = c.location_ID
           ORDER BY b.average
            LIMIT %s
    """, (region, limit))
    result = cursor.fetchall()
    cursor.close()
    connection.close()

    return result


def sort_alphabetically(arg):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""

    """)
    cursor.close()
    connection.close()
