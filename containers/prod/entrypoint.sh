#!/bin/bash
set -e

while ! PGPASSWORD=${POSTGRES_PASSWORD} psql -h ekila-db -U ${POSTGRES_USER} -c '\q'; do
    echo "Waiting for PostgreSQL to start..."
    sleep 1
done
echo "Database is up. Waiting 2 more seconds to ensure readiness..."
sleep 2

if ! PGPASSWORD=${POSTGRES_PASSWORD} psql -U ${POSTGRES_USER} -h ekila-db -p ${POSTGRES_PORT} -lqt | cut -d \| -f 1 | cut -d ' ' -f 2 | grep -q "^${POSTGRES_DB}$"; then
    PGPASSWORD=${POSTGRES_PASSWORD} createdb -U  ${POSTGRES_USER} -h ekila-db -p ${POSTGRES_PORT} ${POSTGRES_DB}
else
    echo "La database existe déjà..."
fi


set a-
source .env
set a+

if [ -f ./ekila/settings_prod.py ]; then
    cp -f ekila/settings_prod_example.py ekila/settings_prod.py
fi

sleep 1
make wait_db
make migrate && make collectstatic

make create-admin
hypercorn ekila.asgi:application --config config/hypercorn.toml
