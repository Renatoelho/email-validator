from pydantic import BaseModel


class Result(BaseModel):
    email: str
    domain_tld: bool
    domain_dns_mx: bool
    syntax: bool
    score: int
    message: str
