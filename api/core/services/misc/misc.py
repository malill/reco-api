from fastapi import Request
import api.core.util.config as cfg

from api.core.db.models.user import BasicUserKeys


def get_user_keys_from_request_header(req: Request) -> BasicUserKeys:
    return BasicUserKeys(cookie=[req.headers.get(cfg.RECO_COOKIE_ID)],
                         canvas=[req.headers.get(cfg.RECO_CANVAS_ID)])
