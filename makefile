.PHONY: run
run:
	uvicorn app:app --reload


.PHONY: makemigration
makemigration:
	$(eval migration?= $(shell bash -c 'read -p "Enter migration description: " comment; echo $$comment'))

	python -m alembic revision --autogenerate -m "migration"