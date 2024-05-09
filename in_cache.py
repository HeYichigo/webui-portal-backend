import json


# <service_id, list[user_ip]
__service_user_mapping: dict[int, list[str]] = {}

# <service_id, count>
__service_count: dict[int, int] = {}


async def entry(service_id: int, user_ip: str):
    ## 更新service_user_mapping
    item = __service_user_mapping.get(service_id)
    if item is None:
        __service_user_mapping[service_id] = []
    __service_user_mapping[service_id].append(user_ip)
    ## 更新service_count
    count = __service_count.get(service_id, 0)
    if count == 0:
        __service_count[service_id] = 0
    __service_count[service_id] += 1


async def exit(service_id: int, user_ip: str):
    ## 更新service_user_mapping
    item = __service_user_mapping.get(service_id)
    if item is not None and len(item) > 0:
        __service_user_mapping[service_id].remove(user_ip)
    ## 更新service_count
    count = __service_count.get(service_id, 0)
    if count > 0:
        __service_count[service_id] -= 1


async def get_service_count(id: int):
    return __service_count.get(id, 0)


async def clear_service_count(id: int):
    __service_count[id] = 0
    __service_user_mapping[id] = []


async def get_service_user_mapping():
    return __service_user_mapping.items()
