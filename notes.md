To Do:


1) dockerize flask app
	expose a port- prob same port it's running on

2) dickerize postgres + create db and tables + load data
-get dockercontainer from postgres
-add lines to import python, psycopg2, pandas

3) try to put the two together

-------------------------------------

input_listings.py:
- remove extra print statements
- user for psql??

build_database.py:
- remove extra print statements
- user for psql??

api.py:
-user for psql??



Working command:
curl -d '{"city": "San Francisco", "state": "CA", "beds": 1}' -H 'Content-Type: application/json' http://127.0.0.1:8088/dataset/common_stats