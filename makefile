.PHONY: run
run:
	uvicorn app:app --reload


.PHONY: makemigration
makemigration:
	$(eval migration?= $(shell bash -c 'read -p "Enter migration description: " comment; echo $$comment'))

	python -m alembic revision --autogenerate -m "$(migration)"

.PHONY: custommigration
custommigration:
	$(eval migration?= $(shell bash -c 'read -p "Enter migration description: " comment; echo $$comment'))
	alembic revision -m "$(migration)"

.PHONY: migrate
migrate:
	alembic upgrade head