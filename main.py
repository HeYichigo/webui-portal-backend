from fastapi import FastAPI, Request, Depends
from db import get_db
import models
from schemas import EntryAndExit, WebUIServiceCreateReq, WebUIServiceResp
from in_cache import entry, exit, get_service_count
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/services", response_model=list[WebUIServiceResp])
async def get_service_list(db: Session = Depends(get_db)):
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
async def entry_service(item: EntryAndExit, req: Request):
    service_id, user_ip = item.service_id, req.client.host
    await entry(service_id, user_ip)
    return await get_service_count(service_id)


@app.post("/exit")
async def exit_service(item: EntryAndExit, req: Request):
    service_id, user_ip = item.service_id, req.client.host
    await exit(service_id, user_ip)
    return await get_service_count(service_id)


@app.post("/reg")
async def reg_service(service: WebUIServiceCreateReq, db: Session = Depends(get_db)):
    models.create_service(db, service)


@app.post("/unreg/{id}")
async def unreg_service(id: int, db: Session = Depends(get_db)):
    return models.delet_service(db, id)
