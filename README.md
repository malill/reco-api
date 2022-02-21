# Recommendation API - Wiki

This repository provides a REST API that exposes calculated recommendations from a **Recommender Builder**. Recommended
items can then be consumed by a recommendation slider carousel to show recommendations.</br>
The API also provides endpoints to collect user evidence, i.e. user behavior that is used for analysis and
recommendation building.

Note that the project structure is based on
[ycd/manage-fastapi][ycd], [tiangolo/full-stack-fastapi-postgresql][tiangolo]
and [markqiu/fastapi-mongodb-realworld-example-app][markqiu]

# System Landscape

![bla](https://docs.google.com/drawings/d/e/2PACX-1vS9i7dEq_v3Q5sZl99youzzXaFWZBnz5ZRjE_02TE-ZGKP8PJQ9QTFmJ8CwUBxbPMEYl1e3bXcJgZCa/pub?w=1440&h=810)

# Installation

## Development

For **local development** use `environment.yml` in order to set up the environment and its specific package
dependencies. Use `conda env create -f environment.yml` from project folder to create the respective environment. To
update the conda environment use the following commands

```shell
conda activate reco-api
conda env update --file environment.yml --prune
```

## Docker

Package dependencies are being installed through requirements.txt also contained in the project folder. To create a new
image (-p x:y means direct local port x to container port y) and run a container:

```shell
docker build -t reco-api .
docker run -d --name reco-api -p 9072:9072 --env-file .env reco-api
```

To build and run docker containers on a RaspberryPi before executing above commands an update of the OS is necessary.

```shell
wget http://ftp.us.debian.org/debian/pool/main/libs/libseccomp/libseccomp2_2.5.1-1_armhf.deb
sudo dpkg -i libseccomp2_2.5.1-1~bpo10+1_armhf.deb
```

# Change History

- Merged `reco-collector` project into `reco-api` since user handling shares too much logic (user creation on both
  services). A user can therefore be created by a single service.
- Added `first_name` and `last_name` to `BasicUserModel`
- Added redirect from `/` to `/docs`
- Created search users by `cookie` function
- Added testing frameworks `pytest[-asyncio][-env]` and basic test functions to repo
- Added `roles` to `BasicUserModel`
- Created `/testing/ab` recommendation endpoint
- Added `groups` attribute to `BasicUserModel`

# References

[markqiu]: https://github.com/markqiu/fastapi-mongodb-realworld-example-app/tree/master/tests

[tiangolo]: https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app

[ycd]: https://github.com/ycd/manage-fastapi

