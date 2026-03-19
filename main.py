import json
import os

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

import models
from db import get_db
from in_cache import (
    clear_service_count,
    entry,
    exit,
    get_service_count,
    get_service_user_mapping,
)
from jwt import decode_jwt_token, encode_jwt_token
from schemas import (
    ChangePasswordReq,
    CreateUserReq,
    EntryAndExit,
    Organization,
    Token,
    WebServiceCreateReq,
    WebServiceResp,
)

app = FastAPI(title="WebUI Portal Backend")

# 先添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 其他 API 路由...
# from .routers import api_router
# app.include_router(api_router, prefix="/api")

# 挂载 Vue 打包的静态文件 - 放在 API 路由之后
# 请确保 vue-dist 目录存在且包含 build 后的文件
VUE_DIST_PATH = os.path.join(os.path.dirname(__file__), "static", "dist")

## db: Session = Depends(get_db)
## _: models.User = Depends(decode_jwt_token)


# 所有 API 路由添加 /api 前缀
@app.get("/api/orgs")
async def get_orgs_list(db: Session = Depends(get_db)):
    return models.get_orgs_list(db)


@app.post("/api/orgs")
async def init_orgs_list(orgs: list[Organization], db: Session = Depends(get_db)):
    models.create_orgs(db, orgs)


@app.post("/api/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    ## 从DB验证用户名密码，成功后编码token发送回客户端
    ## TODO: username -> stu_id
    user = models.get_user_by_stu_id(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect student id or password")
    if not form_data.password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect student id or password")
    token = encode_jwt_token(user.stu_id)
    return Token(access_token=token, token_type="bearer", name=user.name)


@app.post("/api/users")
async def create_user(user: CreateUserReq, req: Request, db: Session = Depends(get_db)):
    db_user = models.get_user_by_stu_id(db, user.stu_id)
    if db_user:
        raise HTTPException(status_code=400, detail="student is already exsite")
    user = models.create_user(db, user, req.client.host)
    return user


@app.get("/api/users")
async def get_user_list(db: Session = Depends(get_db)):
    return models.get_user_list(db)


@app.delete("/api/users/{stu_id}")
async def delete_user(
    stu_id: str,
    db: Session = Depends(get_db),
    _: models.User = Depends(decode_jwt_token),
):
    models.del_user(db, stu_id)


@app.put("/api/users/password")
async def update_password(req_data: ChangePasswordReq, db: Session = Depends(get_db)):
    """
    修改用户密码。
    限制：只有当原密码为默认密码 '123456' 时才允许修改。
    """
    user = models.get_user_by_stu_id(db, req_data.stu_id)
    if not user:
        raise HTTPException(status_code=404, detail="Student ID not found")

    success = models.change_password(
        db, req_data.stu_id, req_data.old_password, req_data.new_password
    )

    if not success:
        # 如果失败，说明原密码不是默认密码 '123456'
        raise HTTPException(
            status_code=400,
            detail="Original password must be the default password to change it.",
        )

    return {"message": "Password updated successfully"}


@app.get("/api/services", response_model=list[WebServiceResp])
async def get_service_list(
    db: Session = Depends(get_db), _: models.User = Depends(decode_jwt_token)
):
    service_list = models.get_service_list(db)
    res = []
    for s in service_list:
        id, name, host, port, url = s.id, s.name, s.host, s.port, s.url
        count = await get_service_count(id)
        item = WebServiceResp(
            id=id, name=name, host=host, port=port, url=url, count=count
        )
        res.append(item)
    return res


@app.post("/api/entry")
async def entry_service(
    item: EntryAndExit, req: Request, _: models.User = Depends(decode_jwt_token)
):
    service_id, user_ip = item.service_id, req.client.host
    await entry(service_id, user_ip)
    return await get_service_count(service_id)


@app.post("/api/exit")
async def exit_service(
    item: EntryAndExit, req: Request, _: models.User = Depends(decode_jwt_token)
):
    service_id, user_ip = item.service_id, req.client.host
    await exit(service_id, user_ip)
    return await get_service_count(service_id)


@app.post("/api/beacon")
async def exit_beacon(req: Request):
    body = await req.body()
    user_ip = req.client.host
    body = json.loads(body)
    await exit(body["service_id"], user_ip)


@app.post("/api/reg")
async def reg_service(service: WebServiceCreateReq, db: Session = Depends(get_db)):
    models.create_service(db, service)


@app.post("/api/unreg/{id}")
async def unreg_service(
    id: int, db: Session = Depends(get_db), _: models.User = Depends(decode_jwt_token)
):
    return models.delet_service(db, id)


@app.post("/api/clear_count/{id}")
async def clear_count(id: int, _: models.User = Depends(decode_jwt_token)):
    await clear_service_count(id)


@app.get("/api/map")
async def get_service_ip_map(_: models.User = Depends(decode_jwt_token)):
    return await get_service_user_mapping()


# 最后挂载 Vue 静态文件，避免拦截 API 路由
if os.path.exists(VUE_DIST_PATH):
    # 将 Vue 应用挂载到根路径，API 路由因有 /api 前缀会优先匹配
    app.mount("/", StaticFiles(directory=VUE_DIST_PATH, html=True), name="vue-app")

else:

    @app.get("/")
    async def root():
        return {"message": "Backend API is running. Vue frontend not deployed yet."}
