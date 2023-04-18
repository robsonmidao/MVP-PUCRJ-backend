from pydantic import BaseModel


class ComentarioSchema(BaseModel):
    """ Define como um novo comentário a ser inserido deve ser representado
    """
    estacionamento_id: int = 1
    texto: str = "Veículo possui arranhões e amassados na porta do motorista."
