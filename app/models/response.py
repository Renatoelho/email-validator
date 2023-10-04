from pydantic import BaseModel


class Response(BaseModel):
    email: str
    domain_tld: bool
    domain_dns_mx: bool
    syntax: bool
    score: int
