.PHONY: build

build:
	docker compose down -v
	docker compose up --build

stop:
	docker compose down