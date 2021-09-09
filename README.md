# Recommendation API - Wiki

This repository provides a REST API that exposes calculated recommendations from **Recommender Builder** (e.g.
see [recommender-system/reco-builder][reco-builder]). Recommended items can then be consumed by
e.g. [Slick Slider][Slick Slider] (see GIF below) to show recommendations.

![Reco Gif](https://santhalus.de/wp-content/uploads/2021/09/reco.gif)

Note that the project structure is based on
[ycd/manage-fastapi][ycd] and [tiangolo/full-stack-fastapi-postgresql][tiangolo].

# Endpoints

## Version 0.1 (`/api/v1`)

### `/unpersonalized/random`

**Parameter** none

**Returns** list of randomly selected products.


### `/unpersonalized/fbt/{item_id_seed}`

**Parameter**
- **item_id_seed** - the item ID that is used for analyzing which items are pairwise bought together in the past, e.g. this
  can be a currently inspected item by the user

**Returns**: list of items that have been bought together with the seed item

# References

Repositories:

- https://github.com/recommender-system/reco-builder
- https://github.com/kenwheeler/slick
- https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app
- https://github.com/ycd/manage-fastapi

[reco-builder]: https://github.com/recommender-system/reco-builder

[Slick Slider]: https://github.com/kenwheeler/slick

[tiangolo]: https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app

[ycd]: https://github.com/ycd/manage-fastapi


<html>

</html>