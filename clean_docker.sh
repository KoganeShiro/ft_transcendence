docker system prune --volumes
docker volume prune
docker volume ls | xargs -r docker volume rm