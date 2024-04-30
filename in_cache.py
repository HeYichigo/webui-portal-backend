import json

# <user_ip, list[service_id]
__user_service_mapping: dict[str, list[int]] = {}

# <service_id, count>
__service_count: dict[int, int] = {}


async def entry(service_id: int, user_ip: str):
    l = __user_service_mapping.get(user_ip, None)
    if l is None:
        __user_service_mapping[user_ip] = []
    __user_service_mapping[user_ip].append(service_id)
    count = __service_count.get(service_id, 0)
    if count == 0:
        __service_count[service_id] = 0
    __service_count[service_id] += 1


async def exit(service_id: int, user_ip: str):
    l = __user_service_mapping.get(user_ip, None)
    if l is not None and len(l) > 0:
        l.remove(service_id)
    count = __service_count.get(service_id, 0)
    if count > 0:
        __service_count[service_id] -= 1


async def get_service_count():
    return json.dumps(__service_count)
