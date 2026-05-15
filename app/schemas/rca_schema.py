from pydantic import BaseModel


class RCARequest(BaseModel):
    query: str
