from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import Session

import schemas
from db import Base, engine


class WebService(Base):
    __tablename__ = "web_service"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String)
    host = Column(String)
    port = Column(Integer)
    url = Column(String)


class User(Base):
    __tablename__ = "user_info"

    stu_id = Column(String, primary_key=True)
    password = Column(String)
    name = Column(String)
    ip = Column(String)
    enabled = Column(Boolean)
    class_name = Column(String)


class Organization(Base):
    __tablename__ = "webui_organization"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    institution = Column(String)
    department = Column(String)
    domain = Column(String)


## create tables
Base.metadata.create_all(bind=engine)


def create_orgs(db: Session, orgs: list[schemas.Organization]):
    orgs_list = []
    for item in orgs:
        ins, dep, dom = item.institution, item.department, item.domain
        org = Organization(institution=ins, department=dep, domain=dom)
        i = db.query(Organization).filter(Organization.domain == org.domain).first()
        if i is None:
            orgs_list.append(org)
    db.add_all(orgs_list)
    db.commit()


def get_orgs_list(db: Session):
    return db.query(Organization).all()


def create_user(db: Session, userinfo: schemas.CreateUserReq, ip: str):
    stu_id, password, name, class_name = (
        userinfo.stu_id,
        userinfo.password,
        userinfo.name,
        userinfo.class_name,
    )
    user = User(
        stu_id=stu_id,
        password=password,
        name=name,
        ip=ip,
        class_name=class_name,
        enabled=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def del_user(db: Session, stu_id: str):
    user = get_user_by_stu_id(db, stu_id)
    db.delete(user)
    db.commit()


def get_user_by_stu_id(db: Session, stu_id: str):
    return db.query(User).filter(User.stu_id == stu_id).first()


def get_user_list(db: Session):
    return db.query(User).all()


def change_password(db: Session, stu_id: str, old_password: str, new_password: str) -> bool:
    """
    修改用户密码。
    条件：原密码必须为默认密码 '123456'。
    返回：如果修改成功返回 True，如果用户不存在或原密码不匹配返回 False。
    """
    user = get_user_by_stu_id(db, stu_id)
    if not user:
        return False
    
    # 检查原密码是否为默认密码
    if user.password != "123456":
        return False
    
    # 执行更新
    user.password = new_password
    db.commit()
    db.refresh(user)
    return True


def get_service_list(db: Session) -> list[WebService]:
    return db.query(WebService).all()


def create_service(db: Session, service: schemas.WebServiceCreateReq):
    name, host, port, url = service.name, service.host, service.port, service.url
    db_service = WebService(name=name, host=host, port=port, url=url)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def delet_service(db: Session, service_id: int):
    service = db.query(WebService).filter(WebService.id == service_id).first()
    db.delete(service)
    db.commit()
