from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    name: str


class Organization(BaseModel):
    institution: str
    department: str
    domain: str


class CreateUserReq(BaseModel):
    stu_id: str
    password: str
    name: str
    class_name: str


class LoginReq(BaseModel):
    stu_id: str
    password: str


class WebServiceResp(BaseModel):
    id: int
    name: str
    host: str
    port: int
    url: str
    count: int


class WebServiceCreateReq(BaseModel):
    name: str
    host: str
    port: int
    url: str


class EntryAndExit(BaseModel):
    service_id: int
