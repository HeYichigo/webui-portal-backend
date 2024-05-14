from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class Organization(BaseModel):
    institution: str
    department: str
    domain: str


class CreateUserReq(BaseModel):
    username: str
    password: str
    org_id: int


class LoginReq(BaseModel):
    username: str
    password: str


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
