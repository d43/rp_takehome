import psycopg2
import os


def create_database(user, db_name='lovely'):
    '''
    Connect to postgres, drop database if exists,
    create database.

    Input:
    - Name of database (optional)

    Output:
    - None
    '''
    try:
        conn = psycopg2.connect(dbname='postgres',
                                user=user,
                                host='localhost')
    except:
        conn = None
        print "I am unable to connect to the database."

    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("DROP DATABASE IF EXISTS " + db_name + ";")
    cur.execute("CREATE DATABASE " + db_name + ";")
    cur.close()
    conn.close()


def connect_database(user, db_name='lovely'):
    '''
    Connects to database, returns connection.

    Input:
    - Psycopg2 connection to database

    Output:
    - Connection (conn)
    '''

    try:
        conn = psycopg2.connect(dbname=db_name,
                                user=user,
                                host='localhost')

    except:
        conn = None
        print "I am unable to connect to the database."

    return conn


def create_listings_table(conn, cur):
    '''
    Input: None
    Output: None

    Create postgres table
    '''

    cur.execute('''
        DROP TABLE IF EXISTS listings;

        CREATE TABLE listings (id serial,
                            beds int,
                            price int,
                            abstract varchar,
                            city varchar,
                            state varchar(2),
                            create_date timestamp,
                            expire_date timestamp,
                            listing_source varchar,
                            PRIMARY KEY (beds, abstract, city, state)
                            );
    ''')
    conn.commit()


if __name__ == "__main__":
    user = os.getlogin()
    create_database(user)
    conn = connect_database(user)

    if conn:
        cur = conn.cursor()
        create_listings_table(conn, cur)
