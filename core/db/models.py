from sqlalchemy import Column, Integer, String, ForeignKey, Float, TIMESTAMP
from sqlalchemy.orm import relationship

from core.constants import DATABASE_TABLE_CONTENT, DATABASE_TABLE_RECS_FBT, DATABASE_TABLE_RECS_ICF
from core.db.database import Base, engine


# TODO: superclass Recommendation_Item for FBT, ICF etc.


class Item(Base):
    __tablename__ = DATABASE_TABLE_CONTENT

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    product_url = Column(String)
    image_url = Column(String)
    creation_time = Column(TIMESTAMP)


class FBT(Base):
    """ frequently bought together"""
    __tablename__ = DATABASE_TABLE_RECS_FBT

    item_id_seed = Column(Integer, primary_key=True)
    item_id_recommended = Column(Integer, ForeignKey(f"{DATABASE_TABLE_CONTENT}.id"), primary_key=True)

    confidence = Column(Float)
    support = Column(Float)

    item = relationship("Item")

    # TODO: create a model package that can be used by both reco-builder, reco-api & reco-adapter-api (otherwise CODE
    #  DUPLICATE) --> maybe not since reco-api needs less info from recommendations table but info from products
    #  table (see next)


class ICF(Base):
    """ item based collaborative filtering """
    __tablename__ = DATABASE_TABLE_RECS_ICF

    item_id_seed = Column(Integer, primary_key=True)
    item_id_recommended = Column(Integer, ForeignKey(f"{DATABASE_TABLE_CONTENT}.id"), primary_key=True)

    similarity = Column(Float)

    item = relationship("Item")
    # CODE DUPLICATE OF DOOM


Base.metadata.create_all(bind=engine)
