from pydantic import BaseModel
from typing import Optional, List
from model.estacionamento import Estacionamento

from schemas import ComentarioSchema


class EstacionamentoSchema(BaseModel):
    """ Define como um novo registro de estacionamento a ser inserido deve ser representado
    """
    placa: str = "ABC-1234"
    veiculo: str = "Nome do Veículo"
    data_hora_entrada: str = "01/01/2023 10:00"
    data_hora_saida:Optional[str] = "01/01/2023 16:00"
    valor: float = 25.00    

class EstacionamentoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base na placa do registro de estacionamento.
    """
    placa: str = "ABC-1234"

class EstacionamentoBuscaExclusaoSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do registro de estacionamento.
    """
    id: int 

class ListagemEstacionamentoSchema(BaseModel):
    """ Define como uma listagem de registro de estacionamento será retornada.
    """
    estacionamentos:List[EstacionamentoSchema]


def apresenta_estacionamentos(estacionamentos: List[Estacionamento]):
    """ Retorna uma representação do registro de estacionamento seguindo o schema definido em
        EstacionamentoViewSchema.
    """
    result = []
    for estacionamento in estacionamentos:
        result.append({
            "id": estacionamento.id,
            "placa": estacionamento.placa,
            "veiculo": estacionamento.veiculo,
            "data_hora_entrada": estacionamento.data_hora_entrada,
            "data_hora_saida": estacionamento.data_hora_saida,
            "valor": estacionamento.valor,
        })

    return {"estacionamentos": result}


class EstacionamentoViewSchema(BaseModel):
    """ Define como um estacionamento será retornado: estacionamento + comentários.
    """
    id: int = 1
    placa: str = "ABC-1234"
    veiculo: str = "Nome do Veículo"
    data_hora_entrada: str = "01/01/2023 10:00"
    data_hora_saida: Optional[str] = "01/01/2023 16:00"
    valor: float = 25.00
    total_comentarios: int = 1
    comentarios:List[ComentarioSchema]


class EstacionamentoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    id: int
   

def apresenta_estacionamento(estacionamento: Estacionamento):
    """ Retorna uma representação do registro de estacionamento seguindo o schema definido em
        EstacionamentoViewSchema.
    """
    return {
        "id": estacionamento.id,
        "placa": estacionamento.placa,
        "veiculo": estacionamento.veiculo,
        "data_hora_entrada": estacionamento.data_hora_entrada,
        "data_hora_saida": estacionamento.data_hora_saida,
        "valor": estacionamento.valor,
        "total_comentarios": len(estacionamento.comentarios),
        "comentarios": [{"texto": c.texto} for c in estacionamento.comentarios]
    }
