#!/usr/bin/env bash
#
# This file is for use with the tiangolo/uvicorn-gunicorn-fastapi:python3.11 only
#
set -e

echo "Sleeping for 10 seconds to allow Maria DB to start..."
sleep 10;

cat << EOF >> /etc/bash.bashrc
alias ls='ls -la'
alias bb-mysql="mysql -u$MYSQL_USER -p${MYSQL_PASSWORD} -h${MYSQL_HOSTNAME} ${MYSQL_DATABASE}"
EOF

# temporary solution to bootstrapping db
echo "Checking if bootstrap file ${MILESTONES_BOOTSTRAP} exists"
if [ -f "${MILESTONES_BOOTSTRAP}" ]; then
    echo "Bootstrapping ${MYSQL_DATABASE} with SQL file ${MILESTONES_BOOTSTRAP}..."
    mysql -u${MYSQL_USER} -p${MYSQL_PASSWORD} -h${MYSQL_HOSTNAME} ${MYSQL_DATABASE} < ${MILESTONES_BOOTSTRAP}
else
    echo "Bootstrap file ${MILESTONES_BOOTSTRAP} does not exist, skipping database bootstrapping..."
fi

INI_FILE="alembic.ini"
if [ -f "${INI_FILE}" ]; then
    echo "${INI_FILE} exists, getting alembic ready..."

    export CONN="sqlalchemy.url = mysql+pymysql\:\/\/${MYSQL_USER}\:${MYSQL_PASSWORD}\@${MYSQL_HOSTNAME}\:${MYSQL_PORT}\/${MYSQL_DATABASE}"

    # back up original ini file for good measure
    cp ${INI_FILE} ${INI_FILE}.bak
    echo "Setting alembic connection string to use env vars for sqlalchemy.url..."
    
    # replace the connection string with the new connection string
    sed -i "s/sqlalchemy.url.*/$CONN/" ${INI_FILE}

    echo "Running alembic migrations..."
    alembic upgrade head
fi