docker stop api-source-etl-scripts-twitter
docker stop api-source-etl-scripts-csv
docker stop logstash-service-etl-twitter
docker stop logstash-service-etl-csv

git pull origin master

mode=twitter docker-compose up --build -d api-source-etl-scripts
mode=csv docker-compose up --build -d api-source-etl-scripts
