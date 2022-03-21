#!/bin/bash

PATH_APPS="."
APPS="main:app"

echo "uvicorn --app-dir ${PATH_APPS} ${APPS}"
uvicorn --app-dir ${PATH_APPS} ${APPS}
