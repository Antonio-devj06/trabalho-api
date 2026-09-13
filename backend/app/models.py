from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.database import Base

class Viagem(Base):
    __tablename__ = "viagens"

    id = Column(Integer, primary_key=True, index=True)

    destino = Column(String, nullable=False)

    motivo = Column(String, nullable=False)

    funcionario = Column(String, nullable=False)

    status = Column(String, nullable=False)