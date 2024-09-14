## Installation

# create docker volume

docker volume create fin_db_vol

# build mysql-db on localhost:3311

docker compose -f "src/docker/docker-compose_database.yml" up -d --build

# setup database

----

## Functions

# Correlation

calculating the performance, vola, correlation based on 1y data between the different assets