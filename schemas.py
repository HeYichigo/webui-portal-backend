from pydantic import BaseModel


class WebUIServiceResp(BaseModel):
    id: int
    host: str
    port: int
    count: int


class WebUIServiceCreateReq(BaseModel):
    host: str
    port: int


class EntryAndExit(BaseModel):
    service_id: int
