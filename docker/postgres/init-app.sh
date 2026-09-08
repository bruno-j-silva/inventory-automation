#!/bin/sh
set -eu
# psql reads the password from the environment; it is never printed or passed as an argument.
APP_DB_PASSWORD="$(cat /run/inventory-postgres/app_db_password)"
export APP_DB_PASSWORD
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<'SQL'
CREATE EXTENSION IF NOT EXISTS pgcrypto;
\getenv app_password APP_DB_PASSWORD
CREATE ROLE inventory_app LOGIN PASSWORD :'app_password';
GRANT USAGE ON SCHEMA public TO inventory_app;
GRANT CREATE ON SCHEMA public TO inventory_app;
SQL
unset APP_DB_PASSWORD
