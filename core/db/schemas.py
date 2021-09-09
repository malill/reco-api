import logging
from pydantic import BaseModel, validator


class ItemBase(BaseModel):
    name: str
    price: str  # force two decimals
    # todo: replace product placeholder url
    product_url = "#"
    # todo: replace image placeholder url
    image_url = "https://img.fcbayern.com/image/upload/q_auto,f_auto/h_300," \
                "c_pad/eCommerce/produkte/28757/t-shirt-upamecano.jpg "

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
