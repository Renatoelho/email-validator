from pydantic import BaseModel


class Payload(BaseModel):
    email: str
