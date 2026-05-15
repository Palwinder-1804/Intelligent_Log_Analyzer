from pydantic import BaseModel


class IncidentExplainRequest(BaseModel):
    query: str


class IncidentExplainResponse(BaseModel):
    explanation: str