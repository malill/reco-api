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

# Change History

- Merged `reco-collector` project into `reco-api` since user handling shares too much logic (user creation on both
  services). A user can therefore be created by a single service.
- Added `first_name` and `last_name` to `BasicUserModel`
- Added redirect from `/` to `/docs`
- Created search users by `cookie` function
- Added testing frameworks `pytest[-asyncio][-env]` and basic test functions to repo
- Added `roles` to `BasicUserModel`
- Created `/testing/ab` recommendation endpoint

# References

[markqiu]: https://github.com/markqiu/fastapi-mongodb-realworld-example-app/tree/master/tests

[tiangolo]: https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app

[ycd]: https://github.com/ycd/manage-fastapi

