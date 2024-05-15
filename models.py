from sqlalchemy import Boolean, Column, Integer, String
from db import Base, engine
from sqlalchemy.orm import Session
import schemas


class WebUIService(Base):
    __tablename__ = "webui_service"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String)
    host = Column(String)
    port = Column(Integer)
    url = Column(String)


class User(Base):
    __tablename__ = "webui_user"

    username = Column(String, primary_key=True)
    password = Column(String)
    name = Column(String)
    ip = Column(String)
    enabled = Column(Boolean)
    org_id = Column(Integer)


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
    username, password, name, org_id = (
        userinfo.username,
        userinfo.password,
        userinfo.name,
        userinfo.org_id,
    )
    user = User(
        username=username,
        password=password,
        name=name,
        ip=ip,
        org_id=org_id,
        enabled=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def del_user(db: Session, username: str):
    user = get_user_by_username(db, username)
    db.delete(user)
    db.commit()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_list(db: Session):
    return db.query(User).all()


def get_service_list(db: Session) -> list[WebUIService]:
    return db.query(WebUIService).all()


def create_service(db: Session, service: schemas.WebUIServiceCreateReq):
    name, host, port, url = service.name, service.host, service.port, service.url
    db_service = WebUIService(name=name, host=host, port=port, url=url)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def delet_service(db: Session, service_id: int):
    service = db.query(WebUIService).filter(WebUIService.id == service_id).first()
    db.delete(service)
    db.commit()
