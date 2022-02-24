from __future__ import division
from scipy.sparse import csr_matrix
import numpy as np
import pandas as pd
import api.core.util.config as cfg
from api.core.db.models.recommendation import CollaborativeFilteringRec
from api.core.services.builder import BaseRecoBuilder
from api.core.util.config import COLLECTION_NAME_RECOMMENDATIONS


class CollaborativeFilteringBuilder(BaseRecoBuilder[CollaborativeFilteringRec]):
    def __init__(self, df, item_based=True):
        super().__init__(collection_name=COLLECTION_NAME_RECOMMENDATIONS)

        self.df = df
        self.d = None
        self.item_based = item_based
        self.map_u = {}
        self.map_l = {}
        self.rating_matrix = None
        self.similarity = None

    def run(self):
        self.create_ratings_matrix()
        self.similarity = self.pairwise_jacquard()
        self.recs = self.sort_similarity()

    def create_ratings_matrix(self):
        # Group interactions
        users_locations = self.df.groupby(
            by=[cfg.COLUMN_USER_ID, cfg.COLUMN_ITEM_ID]).apply(lambda y: 1).to_dict()

        # Number of different Users / Locations
        nu = len(self.df[cfg.COLUMN_USER_ID].unique())
        ni = len(self.df[cfg.COLUMN_ITEM_ID].unique())

        # Build Rating matrix
        row, col = zip(*(users_locations.keys()))  # row-> users,  col-> items
        self.map_u = dict(zip(self.df[cfg.COLUMN_USER_ID].unique(), range(nu)))
        self.map_l = dict(zip(self.df[cfg.COLUMN_ITEM_ID].unique(), range(ni)))
        row_idx = [self.map_u[u] for u in row]
        col_idx = [self.map_l[i] for i in col]
        data = np.array(list(users_locations.values()), dtype=np.float32)
        self.rating_matrix = csr_matrix((data, (row_idx, col_idx)), shape=(nu, ni))

    def pairwise_jacquard(self):
        """Calculates the jacquard sim only on items where at least one item is rated (=1)
        https://stackoverflow.com/questions/32805916/compute-jaccard-distances-on-sparse-matrix
        """
        if self.item_based:
            self.rating_matrix = self.rating_matrix.T

        self.rating_matrix = self.rating_matrix.astype(bool).astype(int)

        intersect = self.rating_matrix.dot(self.rating_matrix.T)  # how many 1s two users have in common
        row_sums = intersect.diagonal()  # how many 1s for each user
        unions = row_sums[:, None] + row_sums - intersect  # (no.user1 + no.user2) - no.together
        return intersect / unions

    def sort_similarity(self):
        self.d = pd.DataFrame(self.similarity)
        self.d.values[[np.arange(self.d.shape[0])] * 2] = 0  # sets diagonal to 0

        recs_dict = []

        key_list = list(self.map_l.keys())

        for col in self.d:
            n_recos = 10
            for i, s in self.d[col].nlargest(n_recos).iteritems():
                recs_dict.append((key_list[col], key_list[i], s))
        recs = self.convert_to_models(recs_dict)
        return recs

    def convert_to_models(self, recs_dict):
        a = [dict(zip(cfg.COLUMNS_RECS_ICF, values)) for values in recs_dict]
        s = []
        for b in a:
            c = dict(b)
            c["base"] = "item"
            rec = CollaborativeFilteringRec(**c, type=cfg.TYPE_COLLABORATIVE_FILTERING)
            s.append(rec)
        return s
