from sqlalchemy import Column, Integer, String
from db import Base, engine
from sqlalchemy.orm import Session
import schemas


class WebUIService(Base):
    __tablename__ = "webui_service"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    host = Column(String)
    port = Column(Integer)


## create tables
Base.metadata.create_all(bind=engine)


def get_service_list(db: Session) -> list[WebUIService]:
    return db.query(WebUIService).all()


def create_service(db: Session, service: schemas.WebUIServiceCreateReq):
    host, port = service.host, service.port
    db_service = WebUIService(host=host, port=port)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def delet_service(db: Session, service_id: int):
    service = db.query(WebUIService).filter(WebUIService.id == service_id).first()
    db.delete(service)
    db.commit()
