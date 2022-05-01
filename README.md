# simplefeed.cloud

# How to Deploy simplefeed.cloud

1. Execute `deploy.py` to copy required files to start `simplefeed.cloud`
2. Build and run containers
3. Connect to webapi
4. Create and apply migration script for database
5. Test simplefeed.cloud


## 1 Execute `deploy.py` to copy required files to start `simplefeed.cloud`
### arguments
- `--target` *(Required)* specify the location where to deploy
- `--db_path` *(Optional)* override the default path for database files 
- `--files_and_dirs` *(Optional)* override the default list of files and dirs to copy to the target location
- `--env_file` *(Optional)* override the default environment yaml file 
- `--docker_env` *(Optional)* override the default docker environment yaml file
- `--config_file` *(Optional)* override the default settings by providing a yaml file

> Example with target = /deploy/simple-feed.cloud-test

```shell
python deploy.py --target /tmp/deploy/simple-feed.cloud-test
```

Output
```shell
SUCCESS Create directory '/tmp/deploy/simple-feed.cloud-test'
SUCCESS Copy directory '/code_dev/projects/halia/simple-feed/alembic' to '/tmp/deploy/simple-feed.cloud-test/alembic'
SUCCESS Copy directory '/code_dev/projects/halia/simple-feed/src' to '/tmp/deploy/simple-feed.cloud-test/src'
SUCCESS Copy directory '/code_dev/projects/halia/simple-feed/templates' to '/tmp/deploy/simple-feed.cloud-test/templates'
SUCCESS Copy file '/code_dev/projects/halia/simple-feed/deploy/docker-compose.yml' to '/tmp/deploy/simple-feed.cloud-test'
SUCCESS Copy file '/code_dev/projects/halia/simple-feed/deploy/Dockerfile' to '/tmp/deploy/simple-feed.cloud-test'
SUCCESS Copy file '/code_dev/projects/halia/simple-feed/deploy/run.sh' to '/tmp/deploy/simple-feed.cloud-test'
SUCCESS Copy file '/code_dev/projects/halia/simple-feed/deploy/env.yml' to '/tmp/deploy/simple-feed.cloud-test'
SUCCESS Copy file '/code_dev/projects/halia/simple-feed/alembic.ini' to '/tmp/deploy/simple-feed.cloud-test'
SUCCESS Copy file '/code_dev/projects/halia/simple-feed/main.py' to '/tmp/deploy/simple-feed.cloud-test'
SUCCESS Copy file '/code_dev/projects/halia/simple-feed/requirements.txt' to '/tmp/deploy/simple-feed.cloud-test'
```

## 2 Build and run containers

```shell
cd /tmp/deploy/simple-feed.cloud-test

docker-compose up

-- or --

docker-compose up --build 

-- or --

docker-compose up --detach

```

## 3.1 Connect to webapi container
```bash
cd /tmp/deploy/simple-feed.cloud-test

docker-compose exec webapi bash
```

## 3.2 Create a migration script for create/update tables in db

```bash
alembic revision --autogenerate -m "Init simplefeed tables"
```

Output
```shell
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'feed'
  Generating /code/alembic/versions/4fddfe689110_init_simplefeed_tables.py ...  done

```

## 3.3 Apply migration script
```shell
alembic upgrade head
```
Output
```shell
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 4fddfe689110, Init simplefeed tables

```