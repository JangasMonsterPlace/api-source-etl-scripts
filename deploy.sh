docker stop api-source-etl-scripts-twitter
docker stop api-source-etl-scripts-csv
docker stop logstash-service-etl

git pull origin master

docker-compose up -d
