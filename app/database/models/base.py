from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    id: int | None = None

    def to_dict(self):
        return self.model_dump()
