# Changelog :arrows_counterclockwise:

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
- Use `reco2js_id` as deterministic user search (:exclamation:)
- Add get item by ID route
- Create attribute `created_time` for `BasicItemModel` and use for latest items route
- Create delete by user uid for evidence
- Store device info at user and not at evidence

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