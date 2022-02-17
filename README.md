# Recommendation API - Wiki

This repository provides a REST API that exposes calculated recommendations from a **Recommender Builder**. Recommended
items can then be consumed by a recommendation slider carousel to show recommendations.

Note that the project structure is based on
[ycd/manage-fastapi][ycd] and [tiangolo/full-stack-fastapi-postgresql][tiangolo].

# Endpoints

## Version 1.0 (`/api/v1`)

tbd

# Change History

- Merged `reco-collector` project into `reco-api` since user handling shares too much logic (user creation on both
  services). A user can therefore be created by a single service.
- Added `first_name` and `last_name` to `BasicUserModel`

# References

[tiangolo]: https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app

[ycd]: https://github.com/ycd/manage-fastapi

