from pydantic import BaseModel


class ModelBase(BaseModel):
    pass
    # id: str | None


class ModelPublic(ModelBase):

    uri: str
    deployed: bool
