export PYTHONUNBUFFERED=1
export PYTHONPYCACHEPREFIX="/.cache/pycache/"

all: wait_for_it run


wait_for_it:
	chmod +x ./wait-for-it.sh
	./wait-for-it.sh -t 120 mad_postgres_service:5432


run:
	python3 main.py


install:
	python3 -m pip install -r requirements.txt


# docker-compose exec db_service alembic init -t async migrations