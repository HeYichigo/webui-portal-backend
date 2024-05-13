from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm
from db import get_db
from jwt import decode_jwt_token, encode_jwt_token
import models
from schemas import (
    CreateUserReq,
    EntryAndExit,
    Token,
    WebUIServiceCreateReq,
    WebUIServiceResp,
)
from in_cache import (
    entry,
    exit,
    get_service_count,
    clear_service_count,
    get_service_user_mapping,
)
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    ## 从DB验证用户名密码，成功后编码token发送回客户端
    user = models.get_user_by_username(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not form_data.password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = encode_jwt_token(user.username)
    return Token(access_token=token, token_type="bearer")


@app.get("/users/me")
async def read_users_me(user: models.User = Depends(decode_jwt_token)):
    return user


@app.post("/users")
async def create_user(user: CreateUserReq, req: Request, db: Session = Depends(get_db)):
    user = models.create_user(db, user, req.client.host)
    return user


@app.get("/users")
async def get_user_list(db: Session = Depends(get_db)):
    return models.get_user_list(db)


@app.get("/services", response_model=list[WebUIServiceResp])
async def get_service_list(
    db: Session = Depends(get_db), _: models.User = Depends(decode_jwt_token)
):
    service_list = models.get_service_list(db)
    res = []
    for s in service_list:
        id, name, host, port, url = s.id, s.name, s.host, s.port, s.url
        count = await get_service_count(id)
        item = WebUIServiceResp(
            id=id, name=name, host=host, port=port, url=url, count=count
        )
        res.append(item)
    return res


@app.post("/entry")
async def entry_service(
    item: EntryAndExit, req: Request, _: models.User = Depends(decode_jwt_token)
):
    service_id, user_ip = item.service_id, req.client.host
    await entry(service_id, user_ip)
    return await get_service_count(service_id)


@app.post("/exit")
async def exit_service(
    item: EntryAndExit, req: Request, _: models.User = Depends(decode_jwt_token)
):
    service_id, user_ip = item.service_id, req.client.host
    await exit(service_id, user_ip)
    return await get_service_count(service_id)


@app.post("/beacon")
async def exit_beacon(req: Request):
    body = await req.body()
    user_ip = req.client.host
    body = json.loads(body)
    await exit(body["service_id"], user_ip)


@app.post("/reg")
async def reg_service(
    service: WebUIServiceCreateReq,
    db: Session = Depends(get_db),
    _: models.User = Depends(decode_jwt_token),
):
    models.create_service(db, service)


@app.post("/unreg/{id}")
async def unreg_service(
    id: int, db: Session = Depends(get_db), _: models.User = Depends(decode_jwt_token)
):
    return models.delet_service(db, id)


@app.post("/clear_count/{id}")
async def clear_count(id: int, _: models.User = Depends(decode_jwt_token)):
    await clear_service_count(id)


@app.get("/map")
async def get_service_ip_map(_: models.User = Depends(decode_jwt_token)):
    return await get_service_user_mapping()
