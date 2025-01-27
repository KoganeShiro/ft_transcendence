# sudo docker build . --tag 42nginx:latest

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
	@echo "  up             Start services in detached mode"
	@echo "  down           Stop and remove containers, networks, and volumes"
	@echo "  restart        Restart the services"
	@echo "  logs           View logs from services"	
	@echo "  clean          Remove all unused Docker resources"
	@echo "  fclean         Remove all unused Docker resources and volumes"

# Build the Docker images
.PHONY: ssl
ssl:
	mkdir -p webserver/certs
	openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout webserver/certs/ft_transcendence.key -out webserver/certs/ft_transcendence.crt -subj "/C=FR/ST=S-M/L=LeHavre/O=42/OU=42/CN=localhost"

.PHONY: rm_ssl
rm_ssl:
	rm -Rf webserver/certs	


.PHONY: build
build:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) build

# Start the services in detached mode
.PHONY: up
up: ssl
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d

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
fclean: down clean rm_ssl
	$(DOCKER) system prune -af --volumes
	@if [ -n "$(shell docker volume ls -q)" ]; then \
		echo "Removing unused volumes..."; \
		docker volume ls -q | xargs docker volume rm; \
	else \
		echo "No volumes to prune."; \
	fi	
		
