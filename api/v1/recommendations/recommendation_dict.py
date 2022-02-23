import api.core.util.config as cfg
import api.core.services.recommendations as rec_service

reco_dict = {
    cfg.ITEM_BASED_COLLABORATIVE_FILTERING: rec_service.get_collaborative_filtering_items
}
