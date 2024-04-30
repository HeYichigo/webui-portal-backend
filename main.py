from fastapi import FastAPI, Request
from schema import EntryAndExit
from in_cache import entry, exit, get_service_count

app = FastAPI()


@app.get("/services")
async def get_service_list():
    return await get_service_count()


@app.post("/entry")
async def entry_service(item: EntryAndExit, req: Request):
    service_id, user_ip = item.service_id, req.client.host
    await entry(service_id, user_ip)
    return await get_service_count()


@app.post("/exit")
async def exit_service(item: EntryAndExit, req: Request):
    service_id, user_ip = item.service_id, req.client.host
    await exit(service_id, user_ip)
    return await get_service_count()


@app.post("/reg")
async def reg_service():
    return


@app.post("/unreg")
async def unreg_service():
    return
