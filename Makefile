# sudo docker build . --tag 42nginx:latest
include .env
# Project variables
PROJECT_NAME = ft_transcendence
DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_FILE = docker-compose.yml

DOCKER = docker


# Default target
.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo "Available targets:"
	@echo "  build          Build the Docker images"
	@echo "  up             Build and Start services"
	@echo "  down           Stop and remove containers, networks"
	@echo "  restart        Restart the services"
	@echo "  logs           View logs from services in detached mode"	
	@echo "  clean          Remove all unused Docker resources"
	@echo "  fclean         Remove all unused Docker resources and volumes"
	@echo "  rm_volumes     Remove all unused Docker volumes"
	@echo "  database       Connect to the postgres database"



# Start the services in detached mode
.PHONY: up
up: build
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d
	@echo "go to: https://$(HOSTNAME):$(PORT) 🤩"


.PHONY: build
build: 
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) build

# Stop and remove services
.PHONY: down
down:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down

# Stop services
.PHONY: stop
stop:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) stop

# Restart the services
.PHONY: restart
restart: down up

# View logs
.PHONY: logs
logs:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) logs -f


# Clean unused Docker resources
.PHONY: clean
clean: down
	$(DOCKER) system prune -af

# Clean unused Docker resources
.PHONY: fclean
fclean: down clean 
	$(DOCKER) system prune -af --volumes
	@if [ -n "$(shell docker volume ls -q)" ]; then \
		echo "Removing unused volumes..."; \
		docker volume ls -q | xargs docker volume rm; \
	else \
		echo "No volumes to prune."; \
	fi	
		
.PHONY: rm_volumes
rm_volumes: 	
	@if [ -n "$(shell docker volume ls -q)" ]; then \
		echo "Removing unused volumes..."; \
		docker volume ls -q | xargs docker volume rm; \
	else \
		echo "No volumes to prune."; \
	fi	

.PHONY: database
database:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec postgres psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)