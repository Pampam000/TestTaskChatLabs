FROM postgres:15
COPY cretae_tables.sql insert_data.sql /docker-entrypoint-initdb.d/
