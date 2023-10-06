from pydantic import BaseModel, EmailStr


class SyntaxEmail(BaseModel):
    syntax_email: EmailStr
