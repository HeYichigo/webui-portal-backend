import sqlite3

con = sqlite3.connect("portal.db", check_same_thread=False)

create_webui_service_table = """
    create table if not exisits webui_service(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        host TEXT,
        port INTEGER
    );
"""

## 考虑在内存中维护用户连接，同时考虑线程安全


def get_service_list():
    sql = """
        select * from webui_service
    """
    res = con.execute(sql)
    res_set = res.fetchall()

    return []


def entry_service(service_id: int, user_host: str):

    return


def exit_service(service_id: int, user_host: str):
    return


def reg_service(host: str, port: int):
    # 需要返回注册的服务实例
    return


def unreg_service(service_id: int):
    # 从DB中删除服务信息
    return
