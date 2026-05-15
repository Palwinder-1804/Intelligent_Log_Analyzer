from pydantic import BaseModel
from typing import Optional


class ParsedLogSchema(BaseModel):
    timestamp: Optional[str] = None
    level: Optional[str] = None
    service: Optional[str] = None
    message: Optional[str] = None
    ip_address: Optional[str] = None


class LogResponseSchema(BaseModel):
    id: str
    filename: str
    content_type: str
    uploaded_by: str