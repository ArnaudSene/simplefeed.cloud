#!/bin/bash
# ---------------------------------------------- 
# DEVOPS --
# Script to deploy a postgres container through 
# docker-compose
# ---------------------------------------------- 
# Required directory and UID:GUID
PGADMIN_DIR="pgadmin-data"
PGADMIN_PERM=5050
# Check directory for pgadmin
if [ ! -d ${PGADMIN_DIR} ]
then
	echo "Create directory ${PGADMIN_DIR}"
	mkdir ${PGADMIN_DIR}
fi
# Check permission on pgadmin
if [ "$(ls -n |grep -w ${PGADMIN_DIR}|cut -d" " -f3,4)" != "${PGADMIN_PERM} ${PGADMIN_PERM}" ]
then
    echo "Set permission ${PGADMIN_PERM}:${PGADMIN_PERM} on ${PGADMIN_DIR}"
    sudo chown -R ${PGADMIN_PERM}:${PGADMIN_PERM} ${PGADMIN_DIR}
fi

# Start Container
/usr/bin/docker-compose up
