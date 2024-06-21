
up:
	sudo docker-compose up

upfill: up filldb

down:
	sudo docker-compose down

migratedb:
	-sudo docker-compose exec mad_db_service alembic revision --autogenerate -m "revision_number_$(REVISIONNUMBER)"

upgrade:
	-sudo docker-compose exec mad_db_service alembic upgrade head

dumpdb:
	mv mad_postgres_service/dump.sql mad_postgres_service/dump.sql.back
	docker exec -i mad_postgres_service /bin/bash -c "PGPASSWORD=${PGPASSW} pg_dump --username ${PGUSER} ${PGDB}" > ./mad_postgres_service/dump.sql

restoredb:
	docker exec -i mad_postgres_service /bin/bash -c "PGPASSWORD=${PGPASSW} psql --username ${PGUSER} ${PGDB}" < ./mad_postgres_service/dump.sql