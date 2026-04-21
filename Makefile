.PHONY: build db-build stop

build:
	docker compose down
	docker compose up --build

db-build:
	docker exec -it -w /app rag_api python -m app.db.init_db

stop:
	docker compose down