from pydantic import BaseModel


class Health(BaseModel):
    status: bool
    mensage: str
