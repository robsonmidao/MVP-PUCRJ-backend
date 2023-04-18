from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comentario


class Estacionamento(Base):
    __tablename__ = 'estacionamento'

    id = Column(Integer, primary_key=True)
    placa = Column(String(140), unique=False)
    veiculo = Column(String(256), unique=False)
    data_hora_entrada = Column(String(140))
    data_hora_saida = Column(String(140))
    valor = Column(Float)
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o estacionamento e o comentário.
    # Essa relação é implicita, não está salva na tabela 'estacionamento',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comentarios = relationship("Comentario")

    def __init__(self, placa:str, veiculo:str, data_hora_entrada:str, data_hora_saida:str, valor:float,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um registro de estacionamento

        Arguments:
            placa: placa do veículo.
            veiculo: tipo do veículo.
            data_hora_entrada: Data e hora de entrada do veículo.
            data_hora_saida: Data e hora de saída do veículo.
            valor: valor cobrado pelo período de uso do estacionametno.
        """
        self.placa = placa
        self.veiculo = veiculo
        self.data_hora_entrada = data_hora_entrada
        self.data_hora_saida = data_hora_saida
        self.valor = valor

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário ao registro de estacionamento.
        """
        self.comentarios.append(comentario)

