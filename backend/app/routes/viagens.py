from fastapi import APIRouter
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Viagem
from app.schemas import ViagemCreate
from app.schemas import ViagemUpdate

router = APIRouter(tags=["Viagens"])


@router.post("/viagens")
def criar_viagem(viagem: ViagemCreate):

    db: Session = SessionLocal()

    nova_viagem = Viagem(
        destino=viagem.destino,
        motivo=viagem.motivo,
        funcionario=viagem.funcionario,
        status=viagem.status
    )

    db.add(nova_viagem)
    db.commit()
    db.refresh(nova_viagem)
    from app.rabbitmq import publicar_mensagem

    # Publicar a mensagem no RabbitMQ
    publicar_mensagem(
    "fila_viagens",
    {
        "evento": "viagem_criada",
        "id": nova_viagem.id,
        "destino": nova_viagem.destino
    }
        )

    publicar_mensagem(
    "fila_notificacoes",
    {
        "evento": "notificacao",
        "mensagem": f"Nova viagem criada para {nova_viagem.destino}"
    }
        )

    return nova_viagem


@router.get("/viagens")
def listar_viagens():

    db: Session = SessionLocal()

    return db.query(Viagem).all()


@router.get("/viagens/{viagem_id}")
def buscar_viagem(viagem_id: int):

    db: Session = SessionLocal()

    viagem = db.query(Viagem).filter(
        Viagem.id == viagem_id
    ).first()

    if not viagem:
        raise HTTPException(
            status_code=404,
            detail="Viagem não encontrada"
        )

    return viagem


@router.put("/viagens/{viagem_id}")
def atualizar_viagem(
    viagem_id: int,
    dados: ViagemUpdate
):

    db: Session = SessionLocal()

    viagem = db.query(Viagem).filter(
        Viagem.id == viagem_id
    ).first()

    if not viagem:
        raise HTTPException(
            status_code=404,
            detail="Viagem não encontrada"
        )

    viagem.destino = dados.destino
    viagem.motivo = dados.motivo
    viagem.funcionario = dados.funcionario
    viagem.status = dados.status

    db.commit()
    db.refresh(viagem)

    return viagem


@router.delete("/viagens/{viagem_id}")
def deletar_viagem(viagem_id: int):

    db: Session = SessionLocal()

    viagem = db.query(Viagem).filter(
        Viagem.id == viagem_id
    ).first()

    if not viagem:
        raise HTTPException(
            status_code=404,
            detail="Viagem não encontrada"
        )

    db.delete(viagem)
    db.commit()

    return {
        "mensagem": "Viagem removida com sucesso"
    }