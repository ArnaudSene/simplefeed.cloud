#!/bin/bash

PATH_APPS="."
APPS="main:app"
PORT="8000"

echo "uvicorn --app-dir ${PATH_APPS} ${APPS} --port ${PORT}"
uvicorn --app-dir ${PATH_APPS} ${APPS} --port ${PORT}
