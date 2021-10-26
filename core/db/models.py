from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from core.constants import DATABASE_TABLE_CONTENT, DATABASE_TABLE_RECS_FBT
from core.db.database import Base, engine


class Item(Base):
    __tablename__ = DATABASE_TABLE_CONTENT

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)


class FBT(Base):
    """ frequently bought together"""
    __tablename__ = DATABASE_TABLE_RECS_FBT

    item_id_seed = Column(Integer, primary_key=True)
    item_id_recommended = Column(Integer, ForeignKey(f"{DATABASE_TABLE_CONTENT}.id"), primary_key=True)

    item = relationship("Item")

    # TODO: create a model package that can be used by both reco-builder and reco-api (otherwise CODE DUPLICATE)
    # --> maybe not since reco-api needs less info from recommendations table but info from products table (see next)


Base.metadata.create_all(bind=engine)
