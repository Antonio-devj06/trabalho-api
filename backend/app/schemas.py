from pydantic import BaseModel


class ViagemBase(BaseModel):
    destino: str
    motivo: str
    funcionario: str
    status: str


class ViagemCreate(ViagemBase):
    pass


class ViagemUpdate(ViagemBase):
    pass


class ViagemResponse(ViagemBase):
    id: int

    class Config:
        from_attributes = True