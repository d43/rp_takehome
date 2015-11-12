To Do:

Dockerfile:
-postgres, psycopg2, my version of python
-load code in
-run code

-get dockercontainer from postgres
-add lines to import python, psycopg2, pandas

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