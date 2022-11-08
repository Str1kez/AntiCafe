env:
	cp .env.example .env

build:
	docker build . -t str1kez/anticafe_backend:latest

up:
	docker compose up -d --remove-orphans

down:
	docker compose down --rmi "local"; docker volume prune -f

swagger:
	docker run -p 80:8080 -e SWAGGER_JSON=/schema.yml -v ${PWD}/openapi-schema.yml:/schema.yml:ro -d --name swagger swaggerapi/swagger-ui

swagger-down:
	docker container rm -f swagger

format:
	poetry run black -S -l 120 .
	poetry run isort .

#.PHONY: format
