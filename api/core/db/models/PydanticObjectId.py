from bson.objectid import ObjectId as BsonObjectId


class PydanticObjectId(BsonObjectId):
    """Wrapper class to set document _id as model attribute.
    See: https://stackoverflow.com/questions/59503461/how-to-parse-objectid-in-a-pydantic-model"""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError('ObjectId required')
        return str(v)
