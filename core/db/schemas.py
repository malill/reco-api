import logging
from pydantic import BaseModel, validator


class ItemBase(BaseModel):
    name: str
    price: str  # force two decimals
    product_url: str
    image_url: str

    @validator('price')
    def check_price(cls, price):
        try:
            return ("%.2f" % float(price)).replace('.', ',')
        except ValueError:
            logging.warning(f"'{price}' can not be transformed into price schema, using db response")
            return price


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True
