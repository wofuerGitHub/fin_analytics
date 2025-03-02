#!/bin/bash

### build-images

docker build --pull --rm -f "src/docker/docker_analyze_assetevaluation" -t fin_analytics_assetevaluation:latest .
docker build --pull --rm -f "src/docker/docker_analyze_correlation" -t fin_analytics_correlation:latest .
docker build --pull --rm -f "src/docker/docker_analyze_optimization_1" -t fin_analytics_optimization_1:latest .
docker build --pull --rm -f "src/docker/docker_analyze_optimization_2" -t fin_analytics_optimization_2:latest .
docker build --pull --rm -f "src/docker/docker_analyze_pvs" -t fin_analytics_pvs:latest .

### build containers

docker compose --project-name "fin" -f "src/docker/docker-compose_analytics.yml" up -d --build

### copy images to host

# docker save fin_analytics_assetevaluation:latest | bzip2 | pv | ssh wolfgang@149.102.143.132 docker load
# docker save fin_analytics_correlation:latest | bzip2 | pv | ssh wolfgang@149.102.143.132 docker load
# docker save fin_analytics_optimization_1:latest | bzip2 | pv | ssh wolfgang@149.102.143.132 docker load
# docker save fin_analytics_optimization_2:latest | bzip2 | pv | ssh wolfgang@149.102.143.132 docker load
# docker save fin_analytics_pvs:latest | bzip2 | pv | ssh wolfgang@149.102.143.132 docker load

### delete old images

# docker rmi $(docker images -f dangling=true -q)
