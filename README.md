# Recommendation API - Wiki

![version](https://img.shields.io/badge/version-0.2-blue)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Docker](https://badgen.net/badge/icon/docker?icon=docker&label)](https://https://docker.com/)

This repository provides a REST API that exposes recommendations from a **Recommender Builder**. Recommended items can
then be consumed by a frontend component to show recommendations.</br>
The API also provides endpoints to collect user evidence, i.e. user behavior that is used for analysis and
recommendation building.</br>
Furthermore, basic recommendation builder services are also included in the repository.

Note that the project structure is based on
[ycd/manage-fastapi][ycd], [tiangolo/full-stack-fastapi-postgresql][tiangolo]
and [markqiu/fastapi-mongodb-realworld-example-app][markqiu].

# System Landscape :mag_right:

The basic recommendation system infrastructure is based on Kim Falk's *Practical Recommender Systems* (2019). The
repository provides services for **evidence collection**, **recommendation building** and **recommendation serving**.

![bla](https://docs.google.com/drawings/d/e/2PACX-1vS9i7dEq_v3Q5sZl99youzzXaFWZBnz5ZRjE_02TE-ZGKP8PJQ9QTFmJ8CwUBxbPMEYl1e3bXcJgZCa/pub?w=1440&h=810)
<figcaption align = "center"><b>Fig.1 - Recommender System Landscape - based on Falk (2019)</b></figcaption>

# Installation :hammer:

For installation, you need to create a `.env` file (check `.env.sample`) and provide following information.

```text
AUTH_USER=****
AUTH_PASS=****

DB_URL=****
DB_NAME=****
```

## Local (conda) :snake:

For local installation with conda use `environment.yml` in order to set up the environment and its specific package
dependencies. Use `conda env create -f environment.yml` from project folder to create the respective environment. To
update the conda environment use the following commands

```shell
conda activate reco-api
conda env update --file environment.yml --prune
```

To run reco-api on port `[PORT]` from command line execute

```shell
uvicorn main:app --reload --port [PORT]
```

## Docker :whale:

Package dependencies are being installed through requirements.txt also contained in the project folder. To create a new
image and run a container:

```shell
docker build -t reco-api .
docker run -d --name reco-api -p [LOCAL_PORT]:9072 --env-file .env reco-api
```

To build and run docker containers on a RaspberryPi before executing above commands an update of the OS is necessary.

```shell
wget http://ftp.us.debian.org/debian/pool/main/libs/libseccomp/libseccomp2_2.5.1-1_armhf.deb
sudo dpkg -i libseccomp2_2.5.1-1~bpo10+1_armhf.deb
```

## Docker Hub :whale2:

The project is also available on *Docker Hub*. A `docker-compose.yml` file to set up a recommender system (no repository
download needed) is provided in the repository (replace credentials where applicable).

```shell
docker-compose up -d
```

# Security :lock:

Basic Authentication is provided for specific routes. Username and password need to be provided in `.env` file
under `AUTH_USER` and `AUTH_PASS`.

# Change History :arrows_counterclockwise:

## Version 1.0 (preview)

- Increased python version `3.8.12`
- Remove unused environment variables
- Add HTTP Basic Auth to specific routes

## Version 0.2

- Merge `reco-builder-api` into project :exclamation:
- Transform routes `POST` to `PUT` where applicable (PUT is used for pure creation of objects, POST for update or
  creation)
- Pytest, ignore DepreciationWarnings
- Added `CollaborativeFilteringBuilder`
- Added `EvidencePipeline` class to fetch evidence synchronous (:exclamation:) from collection for builders
- Created working Collaborative Filtering route
- Fixed recommendation collection storage error
- Added `docker-compose.yml` for fully working recommender system
- Remove collection names from environment
- Fixed missing recommendation service import

## Version 0.1

- Merged `reco-collector` project into `reco-api` since user handling shares too much logic (user creation on both
  services). A user can therefore be created by a single service.
- Added `first_name` and `last_name` to `BasicUserModel`
- Added redirect from `/` to `/docs`
- Created search users by `cookie` function
- Added testing frameworks `pytest[-asyncio][-env]` and basic test functions to repo
- Added `roles` to `BasicUserModel`
- Created `/testing/ab` recommendation endpoint
- Added `groups` attribute to `BasicUserModel`

# References :books:

Falk, Kim. **Practical recommender systems**. Simon and Schuster, 2019.

[markqiu]: https://github.com/markqiu/fastapi-mongodb-realworld-example-app/tree/master/tests

[tiangolo]: https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app

[ycd]: https://github.com/ycd/manage-fastapi

