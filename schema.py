from pydantic import BaseModel


class WebUIService(BaseModel):
    id: int
    host: str
    port: int
    count: int


class EntryAndExit(BaseModel):
    service_id: int
