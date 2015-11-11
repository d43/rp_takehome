import psycopg2
import pandas as pd
import sys
import os


def process_listings(filenames):
    '''
    Input: List of filenames with raw data

    Process: De-duplicate listings on id and (beds/abstract/city/state)
    Keep newest price for each listing (newest create_date)
    Save df as csv

    Output: None
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
    #   Drop duplicates of beds/abstract/city/state
    #   (keep first/newest listing)
    df = df.sort('create_date', ascending=False)
    df.drop_duplicates(subset=['beds', 'abstract', 'city', 'state'],
                       inplace=True)

    # Fill NaN's with acceptable data for db
    # Abstract: "None"
    df.abstract.fillna("None", inplace=True)
    # Expire_date: "1700-01-01T00:00:00.000000000-0000"
    # This is an anomaly that I'll be able to identify later if needed.
    datetime_nan = '1700-01-01T00:00:00.000000000-0000'
    df.expire_date.fillna(datetime_nan, inplace=True)

    df.to_csv("newest_listings.csv", index=False)

    return df.shape[0]


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


def load_listings():
    '''
    Input: De-duplicated dataframe with newest price for each rental
    Output: None

    Output df to csv
    Load csv into postgres
    '''
    file_loc = os.getcwd() + '/newest_listings.csv'

    cur.execute('''
        COPY listings FROM '%s' WITH DELIMITER ',' CSV HEADER;
    ''' % file_loc)

    conn.commit()


if __name__ == "__main__":
    print "Connecting to Database"
    conn = connect_database()

    if conn:
        cur = conn.cursor()
        print "Loading Listings into DB"
        feeds = sys.argv[1:]
        num_listings = process_listings(feeds)
        load_listings()
        print num_listings, "new listings were entered into the database"
