# Recommendation API - Wiki

![version](https://img.shields.io/badge/version-0.2-blue)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Docker](https://badgen.net/badge/icon/docker?icon=docker&label)](https://https://docker.com/)

This repository provides a REST API that exposes recommendations from a **recommender builder**. Recommended items can
then be consumed by a frontend component to show recommendations.

> A **personalized recommendation** is an **item** that is derived from a **relation**. An **item** is an object a
> **user** can interact with, e.g. product, movie, article ... Interaction between **users** and **items** lead to
> **evidence** which can be used to derive further **relations** and therefore more (precise) recommendations.

The API also provides services to collect user evidence, i.e. user behavior that is used for analysis and recommendation
building.</br>
Furthermore, basic recommendation builder services are also included in the repository.

Note that the project structure is based on
[ycd/manage-fastapi][ycd], [tiangolo/full-stack-fastapi-postgresql][tiangolo]
and [markqiu/fastapi-mongodb-realworld-example-app][markqiu].

> Preview: use **reco-js** frontend framework to consume **reco-api**!

# System Landscape :mag_right:

The basic recommendation system infrastructure is based on Kim Falk's *Practical Recommender Systems* (2019). The
repository provides services highlighted in red, i.e. **evidence collection**, **recommendation building** and
**recommendation serving**. Currently, the repository uses MongoDB :leaves: for persistence.

![bla](https://docs.google.com/drawings/d/e/2PACX-1vS9i7dEq_v3Q5sZl99youzzXaFWZBnz5ZRjE_02TE-ZGKP8PJQ9QTFmJ8CwUBxbPMEYl1e3bXcJgZCa/pub?w=1440&h=810)
<figcaption align = "center"><b>Fig.1 - Recommender System Landscape - based on Falk (2019)</b></figcaption>

# Installation :hammer:

For installation, you need to create a `.env` file (check `.env.sample`) and provide following information (replace with
your values respectively).

```text
# Basic Authentification Credentials
AUTH_USER=****
AUTH_PASS=****

# CORS
CORS_ORIGIN_REGEX=https://.*\.example\.org

# MongoDB Connection Settings
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

# Basic Usage

![bla](https://docs.google.com/drawings/d/e/2PACX-1vTmTmiNSEPv2LY3Ns6Nlvq8y0RU_yjIZfMbc6GKX5vi90V-MgO_aThHO4sVFF3GeS4uiNZMqnk5Lce_/pub?w=960&h=720)

# Demo :cd:

Access to a demo version can be found here: https://reco-api-q.herokuapp.com/

# Models :minidisc:

**BasicEvidenceModel**

**BasicItemModel**

**BasicRelationModel**

**BasicSplittingModel**

**BasicUserKeys**
(not persisted)

**BasicUserModel**

# Recommendation Building Methods :construction_worker:

The repository provides basic recommendation building methods.

> Recommendation entries `REs` always inherit from `BasicRecommendationModel`. If a `RecommendationBuilder` creates new
`REs`, old `REs` are kept. Endpoints always return the most recent calculated `REs`.

- **Frequently Bought Together** (tbd)
- **Collaborative Filtering**

# Routes :globe_with_meridians:

The API provides a swagger UI to view all available routes.

## Collection `api/v1/col`

Collection routes include **item**, **user** and **evidence** services.

### Evidence `/evidence` :page_facing_up:

Basic `GET` and `PUT` methods. Note that `PUT` route always consumes a `List` of `BasicEvidenceModels`.

### Item `/item` :shirt:

### User `/user` :raising_hand:

Note that the `GET` method will always return a `BasicUserModel` given a query parameter `cookie_value`. The method
returns an already persisted user who contains a `key` list entry with respective cookie value, or it will create a new
user and set the cookie value.

> Note that this method will be replaced with a probabilistic fetch method. Currently `reco-cookie-id` is a deterministic key to identify users. In the future various keys will be used to identify a user.

## Recommendation `api/v1/rec`

Recommendation routes include **splitting** and **item** services. Different to collection route **item services** from
recommendation route represent **personalized** and **unpersonalized recommendations**.

### Personalized Recommendations Item `/per` :monkey_face:

Utilize the recommendations that can be obtained from **relations** created by the **recommendation builders**.

### Unpersonalized Recommendations Item `/unpers` :see_no_evil:

Utilize the recommendations that can be obtained from the database itself without the user of **relations**. Available
non-personalized methods are:

- latest items
- random items

### Splitting `/split` :left_right_arrow:

*Splitting* refers to testing different recommendation approaches, e.g. A/B testing. You can run A/B tests to evaluate
different recommendation methods. Recommendations retrieved from a splitting setup are called **split recommendations**.

> Splitting is currently only available for users that provide a `reco-user-uid` in their request header. If
> `reco-user-uid` is provided an already existing user will be fetched from DB, a splitting method will be drawn from
> respective `splitting` collection entry and assigned as a `group` entry to the user object, e.g. `{split_name: 'cf_ib'}`.

To create a simple A/B test you have to provide an instance of a `SplittingModel`. To create such an object you can
call `/api/v1/rec/split/conf` and provide a path parameter `name` and request body with a list of recommendation
methods `methods`.

As mentioned it is assumed that a user already exists in DB. **User creation from frontend is expected through
calling `api/v1/col/user`.**

**Error Handling**

- If `reco-user-uid` is not available in request header, the fallback method will be used, a user is **not** created.
- If no user can be found in user collection matching the `reco-user-uid` from request header, the fallback method will
  be used
- If the splitting name from the request query is
    - not found in DB collection, or
    - is found in DB collection but the drawn recommendation method string from the retrieved object is not assigned to
      a recommendation method,

  the fallback method will be used **and** this user will be added to the fallback group for this particular splitting

> To prevent spillover effects (i.e. users switching groups for a particular splitting), group assignments are not 
> updated even when user was assigned to the fallback group. Once a splitting method is assigned to a user it won't
> be changed.

# Security :lock:

Basic Authentication is provided for specific routes. Username and password need to be provided in `.env` file
under `AUTH_USER` and `AUTH_PASS`.

# Change History :arrows_counterclockwise:

## Version 1.0 (preview)

- Increased python version `3.8.12`
- Remove unused environment variables
- Add HTTP Basic Auth to specific routes
- Add test for inserting recs
- Create get all users route
- Add basic A/B testing logic and routes (:exclamation:)
- Move `timestamp`, `item_id_seed` and `item_id_recommended` to parent class `BasicRecommendationModel`
- Rename A/B testing to **splitting**
- Added delete users by cookie value route
- Rename recommendations to relations where applicable
- Fixed missing API response models
- Add flexible search query scripts to project
- Return number inserted evidence objects for PUT route
- Add `keys` attribute to `BasicEvidenceModel` to identify user
- Create `BasicUserKeysModel` to handle user keys
- Add `updateTime` to `BasicUserModel`
- Reduce number of default returned recommendations to 3
- Enable user fetching/inserting for evidence PUT route
- Replace `allow_origins` with `allow_origin_regex` in FastAPI middleware
- Add string representation of user _id to evidence object
- Use user uid in splitting (:exclamation:)

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

