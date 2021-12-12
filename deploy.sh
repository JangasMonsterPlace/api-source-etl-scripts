docker stop api-source-etl-scripts-twitter
docker stop api-source-etl-scripts-csv
docker stop logstash-service-etl

git pull origin master

mode=twitter docker-compose up -d api-source-etl-scripts
mode=csv docker-compose up -d api-source-etl-scripts
docker-compose up -d logstash-service
