.PHONY: help

default: help

start-app: ## start django development server
	python3 manage.py runserver

wait_db: ## test if db is up
	python3 manage.py wait_for_db

migrate: ## run django migrations for DB maintenanbility
	python3 manage.py makemigrations && python3 manage.py migrate

flushdb: ## flush all the db (remove all data in db)
	python3 manage.py flush

collectstatic:  ## collecstatic file and create static folder
	python3 manage.py collectstatic --noinput

create-admin: ## Create Django superuser if not exists
	@USER_EXISTS="from django.contrib.auth import get_user_model; User = get_user_model(); exit(0 if User.objects.filter(is_superuser=True).exists() else 1)"; \
	python3 manage.py shell -c "$$USER_EXISTS" || \
	DJANGO_SUPERUSER_PASSWORD=admin123 python3 manage.py createsuperuser \
		--no-input \
		--username=admin \
		--email=admin@gmail.com \
		|| true
	@echo "Superuser created with username: admin created successfully"

up: ## build and run container compose eg. eg. make up env-target=prod for production eg.make up env-target=prod (for production)
	@if [ "$(env-target)" = "prod" ]; then \
		sudo docker compose -f docker-compose.prod.yml build --no-cache && sudo docker compose -f docker-compose.prod.yml up -d;\
	else \
		sudo docker compose -f docker-compose.dev.yml build --no-cache && sudo docker compose -f docker-compose.dev.yml up -d;\
	fi

down: ## Shut down all container of specific compose
	@if [ "$(env-target)" = "prod" ]; then \
		sudo docker compose -f docker-compose.prod.yml down; \
	else \
		sudo docker compose -f docker-compose.dev.yml down; \
	fi


clear-docker: ## Clear docker cache and volume eg. make make clear-docker env-target=prod for production eg.make up env-target=prod (for production)
	@if [ "$(env-target)" = "prod" ]; then \
		sudo docker buildx prune -f && sudo docker compose -f docker-compose.prod.yml down --volumes; \
	else \
		sudo docker buildx prune -f && sudo docker compose -f docker-compose.dev.yml down --volumes; \
	fi

shell: ## enable django shell
	python3 manage.py shell

help:
	@echo "usage: make [command]"
	@echo ""
	@echo "Website available commands 🚀,if you use windows Damn bruh!!!!:"
	@sed \
    		-e '/^[a-zA-Z0-9_\-]*:.*##/!d' \
    		-e 's/:.*##\s*/:/' \
    		-e 's/^\(.\+\):\(.*\)/$(shell tput setaf 6)\1$(shell tput sgr0):\2/' \
    		$(MAKEFILE_LIST) | column -c2 -t -s :
