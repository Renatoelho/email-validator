from pydantic import BaseModel


class Health(BaseModel):
    status: bool
    message: str
