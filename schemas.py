from pydantic import BaseModel


class WebUIServiceResp(BaseModel):
    id: int
    name: str
    host: str
    port: int
    url: str
    count: int


class WebUIServiceCreateReq(BaseModel):
    name: str
    host: str
    port: int
    url: str


class EntryAndExit(BaseModel):
    service_id: int
