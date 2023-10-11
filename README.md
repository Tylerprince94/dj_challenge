# Description

This project houses a multiservice architecture containing 2 services to determine average
Houston air quality forecast over the next 4 days.

Services:

1. Datajoint enabled mysql db version 5.7: "db"
2. Python app executing simple queries on this db: "pythonapp"
   Execution of this project stands up the empty db instance (no database or table creations) and
   then runs a python script from within the pythonapp.

pythonapp script:

The script is a data pipeline meeting all requirements to the DJ coding challenge. This 
pipeline leverages the requests library to grab publicly available information on pollution 
forecasts in the Houston area, inserts this data to the db using pymysql, reads this data out 
of the db, calculates the averaged forecast over the next four days using pandas, saves that
result into a different table, and then displays the result.

### Build / Rebuild Docker Images (necessary if changes are made to source code or Dockerfile)

1. run `docker-compose build`

### Run

-Prerequisite: Docker / Docker Compose are installed on host machine

1. git clone {https git link}
2. cd into project `cd dj_challenge`
3. run `docker-compose up -d --build`
4. run `docker ps -a`
5. find and copy the container id for dj_challenge1-pythonapp into step 6
6. run `docker logs {container-id}`
7. example output found at supplemental/example_log_output.txt
Note - run `docker-compose down` to stop the services

### Validate MYSQL DB Instance Independent of Python Service Health

-Prerequisite: MYSQL Shell App is installed from internet on host machine

1. Start MYSQL Shell App
2. run `\connect --mysql root@localhost:3306`
3. enter password "simple"
4. run `\sql`
5. run `SELECT user, host, ssl_type, ssl_cipher, account_locked FROM mysql.user;`

### Validate Containers Belong to Same Network

-Prerequisite: "Run" section of this readme has just been executed... (services up)

1. run `docker inspect dj_challenge_default` (or `docker inspect {alt-network-name}`)
2. confirm both services are listed in the "containers" section
