from sqlalchemy import Column, Integer

from core.db.database import Base, engine


class FBT(Base):
    """ (f)requently (b)ought (t)ogether"""
    __tablename__ = 'fbt'

    item_seed_id = Column(Integer, primary_key=True)
    item_recommended_id = Column(Integer, primary_key=True)

    # TODO: create a model package that can be used by both reco-builder and reco-api (otherwise CODE DUPLICATE)
    # --> maybe not since reco-api needs less info from recommendations table but info from products table (see next)
    # TODO: use sqlalchemy.orm.relationship to get item information from another table


Base.metadata.create_all(bind=engine)
