#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER user_test WITH ENCRYPTED PASSWORD 'podemos';

    CREATE DATABASE podemos_pambu;
    CREATE DATABASE podemos_utils;
    CREATE DATABASE podemos_validaciones;
    CREATE DATABASE podemos_digitalizacion;
    CREATE DATABASE podemos_documentos;

    GRANT ALL PRIVILEGES ON DATABASE podemos_pambu TO user_test;
    GRANT ALL PRIVILEGES ON DATABASE podemos_utils TO user_test;
    GRANT ALL PRIVILEGES ON DATABASE podemos_validaciones TO user_test;
    GRANT ALL PRIVILEGES ON DATABASE podemos_digitalizacion TO user_test;
    GRANT ALL PRIVILEGES ON DATABASE podemos_documentos TO user_test;

    GRANT USAGE ON SCHEMA public TO user_test;
EOSQL