# simplefeed.cloud


# How to Deploy simplefeed.cloud

1. Execute `deploy.py` to copy required files to start `simplefeed.cloud`
2. Create a migration script for create/update tables in db
3. Run the migration
4. (Optional) Build manually Docker image for `simplefeed.cloud` api 
5. Start `simplefeed.cloud` apps


## 1. Execute `deploy.py` to copy required files to start `simplefeed.cloud`

> Example with path = /deploy/simple-feed.cloud-test

```shell
python deploy.py -path /deploy/simple-feed.cloud-test
```

```shell
create directory '/deploy/simple-feed.cloud-test'
successfully created!
copy directory '/code_dev/halia/simple-feed/alembic' to '/deploy/simple-feed.cloud-test/alembic'
successfully copied!
copy file '/code_dev/halia/simple-feed/deploy/docker-compose.yml' to '/deploy/simple-feed.cloud-test'
successfully copied!
copy file '/code_dev/halia/simple-feed/deploy/Dockerfile' to '/deploy/simple-feed.cloud-test'
successfully copied!
copy file '/code_dev/halia/simple-feed/deploy/run.sh' to '/deploy/simple-feed.cloud-test'
successfully copied!
copy file '/code_dev/halia/simple-feed/deploy/env.yml' to '/deploy/simple-feed.cloud-test'
successfully copied!
copy directory '/code_dev/halia/simple-feed/src' to '/deploy/simple-feed.cloud-test/src'
successfully copied!
copy directory '/code_dev/halia/simple-feed/templates' to '/deploy/simple-feed.cloud-test/templates'
successfully copied!
copy file '/code_dev/halia/simple-feed/alembic.ini' to '/deploy/simple-feed.cloud-test'
successfully copied!
copy file '/code_dev/halia/simple-feed/main.py' to '/deploy/simple-feed.cloud-test'
successfully copied!
copy file '/code_dev/halia/simple-feed/requirements.txt' to '/deploy/simple-feed.cloud-test'
successfully copied!

```

## 2. Create a migration script for create/update tables in db


```bash
alembic revision --autogenerate -m "Init simplefeed tables"
```



## 3.

## 4. (Optional) Build and run manually Docker image for `simplefeed.cloud` api

### Build Docker image for `simplefeed.cloud` api
```shell
docker build -t simple-feedcloud_webapi .
```
### Run Docker container for `simplefeed.cloud` api
```shell
docker run -d --name simple-feedcloud_webapi_1 -p 80:80 simple-feedcloud_webapi

```



1. Define files and dirs to make a package
2. define execution tasks
3. copy these files and dirs to the new location
4. execute tasks
    - run containers (postgres, pgadmin, webapi)
    - apply alembic migration (create database and table if needed)
