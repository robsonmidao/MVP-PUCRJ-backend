from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base


class Comentario(Base):
    __tablename__ = 'comentario'

    id = Column(Integer, primary_key=True)
    texto = Column(String(4000))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o comentário e um estacionamento.
    # Aqui está sendo definido a coluna 'estacionamento' que vai guardar
    # a referencia ao estacionamento, a chave estrangeira que relaciona
    # um estacionamento ao comentário.
    estacionamento = Column(Integer, ForeignKey("estacionamento.id"), nullable=False)

    def __init__(self, texto:str):
        """
        Cria um Comentário

        Arguments:
            texto: o texto de um comentário.
            data_insercao: data de quando o comentário foi feito ou inserido
                           à base
        """
        self.texto = texto       
        self.data_insercao = datetime.now()
