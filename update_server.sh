# !/bin/bash
dockerFile="docker_analyze_assetevaluation"
imageName="fin_analytics_assetevaluation"
yamlFile="docker-compose_analytics.yml"

# --- local machine ---

# 1: create a new image with the latest code based on linux
# org: docker build --pull --rm -f 'docker_analyze_assetevaluation' -t 'fin_analytics_assetevaluation:latest' '.' 

docker buildx build --platform linux/amd64 --pull --rm -f "$dockerFile" -t "${imageName}:latest" --load '.' 

#2: save the image to a tar file

docker save ${imageName}:latest -o ${imageName}_latest.tar 

#3: copy the tar file to the server

rsync -avz --progress --inplace ${imageName}_latest.tar wolfgang@data.wofuer.com:/home/wolfgang/${imageName}_latest.tar

#4: remove the local tar file
rm ${imageName}_latest.tar

# ---- server ----

# 5: list server containers and stop the current container and remove it; remove unused images

ssh wolfgang@data.wofuer.com "docker ps -a && \
   docker stop ${imageName} || true && \
   docker rm   ${imageName} || true && \
   docker image prune -f || true && \
   docker load -i /home/wolfgang/${imageName}_latest.tar"

# 6: run the new container always at server as manual step

ssh wolfgang@data.wofuer.com "docker compose -f /home/wolfgang/${yamlFile} up -d --build ${imageName}" 