from pydantic import BaseModel


class Errors(BaseModel):
    status: bool
    erro: str