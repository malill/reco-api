import logging

from fastapi import APIRouter

from api.core.services.builder.CollaborativeFilteringBuilder import CollaborativeFilteringBuilder
from api.core.services.evidence import EvidencePipeline
from api.core.util.config import ENDPOINT_BUILDER, TAG_BUILDER

api_router = APIRouter(prefix=ENDPOINT_BUILDER, tags=[TAG_BUILDER])

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@api_router.put("")
def collaborative_filtering(base: str = 'item'):
    logger.info(f"Collaborative filtering endpoint called with based {base}")

    evidence_pipeline = EvidencePipeline()

    collaborative_filtering_builder = CollaborativeFilteringBuilder(df=evidence_pipeline.get_raw_evidence())
    collaborative_filtering_builder.run()
    collaborative_filtering_builder.store_recs()

    return "Hello Builder!"
