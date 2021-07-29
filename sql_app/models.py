from sqlalchemy import Column, Integer, String

from sql_app.database import Base


class Marker(Base):
    __tablename__ = "marker"

    id = Column(Integer, primary_key=True, index=True)
    version = Column(Integer)
    label = Column(String)

    class Config:
        orm_mode = True
