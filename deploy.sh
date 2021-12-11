docker stop api-source-etl-scripts

git pull origin master

docker-compose up --build -d api-source-etl-scripts
