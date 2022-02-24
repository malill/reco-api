import logging

from fastapi import APIRouter, status, Depends
from starlette.responses import JSONResponse

from api.core.services.authentification.basic_auth import check_basic_auth
from api.core.services.builder.CollaborativeFilteringBuilder import CollaborativeFilteringBuilder
from api.core.services.collection.evidence import EvidencePipeline
from api.core.util.config import ENDPOINT_BUILDER, TAG_BUILDER

api_router = APIRouter(prefix=ENDPOINT_BUILDER, tags=[TAG_BUILDER])

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@api_router.put("")
def collaborative_filtering_builder(auth: str = Depends(check_basic_auth),
                                    base: str = 'item'):
    """Runs CF builder and stores reco in db."""
    logger.info(f"Collaborative filtering endpoint called with based {base}")

    evidence_pipeline = EvidencePipeline()

    cfb = CollaborativeFilteringBuilder(df=evidence_pipeline.get_raw_evidence())
    cfb.run()
    cfb.store_recs()

    return JSONResponse(content={'builder': str(cfb.__class__),
                                 'status': 'successful',
                                 'used_evidence_size': len(cfb.df),
                                 'inserted_recs': len(cfb.recs)},
                        status_code=status.HTTP_201_CREATED)
