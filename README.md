# Recommendation API - Wiki

This repository provides a REST API that exposes calculated recommendations from **Recommender Builder** (e.g.
see [recommender-system/reco-builder][reco-builder])

Note that the project structure is based on
[ycd/manage-fastapi][ycd] and [tiangolo/full-stack-fastapi-postgresql][tiangolo].

# Endpoints

## Version 0.1 (`/api/v1`)

### `/fbt/{item_id_seed}`

Params:

- **item_id_seed** - the item that is used for analyzing which items are pairwise bought together in the past, e.g. this
  can be a currently inspected item by the user

# References

Repositories:

- https://github.com/recommender-system/reco-builder
- https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app
- https://github.com/ycd/manage-fastapi

[reco-builder]: https://github.com/recommender-system/reco-builder

[tiangolo]: https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app

[ycd]: https://github.com/ycd/manage-fastapi
