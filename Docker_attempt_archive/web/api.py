from flask import Flask, request, jsonify
import requests
import psycopg2
import os


def start_app(conn):
    '''
    Input:
    - Connection to postgres database

    Output:
    - None

    Boots flask application
    '''

    # Initialize flask app
    app = Flask(__name__)

    # Define routes/pages and get template
    @app.route('/')
    def home():
        return "There's nothing here!"

    @app.route('/dataset/common_stats', methods=['POST'])
    def common_stats():
        if not request.json:
            abort(404)
        city = request.json['city']
        state = request.json['state']
        beds = request.json['beds']
        # test input?

        # Query database and return results
        c = conn.cursor()
        c.execute('''
            SELECT AVG(price) AS average,
                   STDDEV(price) AS stddev,
                   MAX(price) as max,
                   MIN(price) as min,
                   COUNT(price) as count
            FROM listings
            WHERE city = '%s'
            AND state = '%s'
            AND beds = %i
            ;''' % (city, state, beds))
        stat_list = list(c.fetchone())

        # Convert stat_list to json
        output = jsonify({'price': {
                             'mean': stat_list[0],
                             'standard deviation': stat_list[1],
                             'max': stat_list[2],
                             'min': stat_list[3],
                             'count': stat_list[4]
                         }})

        # Return stat_list in json format
        return output

    # Boot application
    app.run(host='127.0.0.1', port=8088, debug=False)


if __name__ == "__main__":
    # Connect to database
    user = os.getlogin()
    conn_dict = {'dbname': 'lovely', 'user': user, 'host': '/tmp'}
    conn = psycopg2.connect(dbname=conn_dict['dbname'],
                            user=conn_dict['user'], host=conn_dict['host'])

    start_app(conn)
