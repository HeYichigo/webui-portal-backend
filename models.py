from sqlalchemy import Column, Integer, String
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


## create tables
Base.metadata.create_all(bind=engine)


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
