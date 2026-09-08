#!/bin/sh
set -eu
# Compose file secrets retain host ownership. Copy privately for the postgres user.
mkdir -p /run/inventory-postgres
chmod 700 /run/inventory-postgres
chown postgres:postgres /run/inventory-postgres
cp /run/secrets/app_db_password /run/inventory-postgres/app_db_password
chown postgres:postgres /run/inventory-postgres/app_db_password
chmod 400 /run/inventory-postgres/app_db_password
exec docker-entrypoint.sh "$@"
