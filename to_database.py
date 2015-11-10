import psycopg2
import pandas as pd

def create_database(db_name='lovely'):
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
                                user='danaezoule',
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

def process_listings(filenames):
    '''
    Input: List of filenames with raw data

    Output: One de-duplicated dataframe, with newest price for each listing
    '''

    # Read in data, add source column, make dates to datetime
    # Note: Date to datetime may be unneccessary
    # Note: listing source field may be unneccessary
    # Put into one dataframe
    df = pd.DataFrame()
    for source in filenames:
        df_input = pd.read_csv(source)
        df_input['source'] = source
        df_input['create_date'] = pd.to_datetime(df_input['create_date'])
        df_input['expire_date'] = pd.to_datetime(df_input['expire_date'])
        df = df.append(df_input)

    # Remove id duplicates
    # Subset argument tested: I get the same results from using 'id'
    # as using all rows except feedsource.
    df.drop_duplicates(subset=['id'], inplace=True)

    # Keep newest price
    #   Sort by create_date (newest listing is now first)
    #   Drop duplicates of beds/abstract/city/state (keep first/newest listing)
    df = df.sort('create_date', ascending=False)
    df.drop_duplicates(subset=['beds', 'abstract', 'city', 'state'], inplace=True)

    return df

def connect_database(db_name='lovely'):
    '''
    Connects to database, returns connection.

    Input:
    - Psycopg2 connection to database

    Output:
    - Connection (conn)
    '''

    try:
        conn = psycopg2.connect(dbname=db_name,
                                user='danaezoule',
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


def load_listings(df):
    '''
    Input: De-duplicated dataframe with newest price for each rental
    Output: None

    Output df to csv
    Load csv into postgres
    '''


    cur.execute('''
        COPY listings FROM %s WITH DELIMITER ',' CSV HEADER;

    ''')

    conn.commit()




if __name__ == "__main__":
    print "Creating Database"
    create_database()
    print "Connecting to Database"
    conn = connect_database()

    if conn:
        cur = conn.cursor()
        print "Creating Listings Table"
        create_listings_table()