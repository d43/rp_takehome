# rp_takehome

Libraries needed:  
	Postgres: http://www.postgresql.org/  
	Psycopg2: http://initd.org/psycopg/  
	Anaconda (Python 2.7, Pandas, Flask, requests): https://www.continuum.io/downloads  

## Steps:

Start Local Postgres Server (GUI)  

From Terminal:  

```bash
python build_database.py
python input_listings.py listings1.csv listings2.csv listings3.csv
python api.py
```

In another terminal:

```bash
curl -d '{"city": "San Francisco", "state": "CA", "beds": 1}' -H 'Content-Type: application/json' http://127.0.0.1:8088/dataset/common_stats
```

Note:
* build_database.py assumes default postgres database name is 'postgres'  
* user name for new database given by os.getlogin()
* Docker attempt files in /Docker_attempt_archive

