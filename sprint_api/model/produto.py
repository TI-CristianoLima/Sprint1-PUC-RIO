from sqlalchemy import Column, String, Integer, DateTime, Float
from datetime import datetime
from typing import Union
from model.base import Base

class Produto(Base):
    __tablename__ = 'produto'

    id = Column("pk_produto", Integer, primary_key=True)
    nome = Column(String(150), unique=True)
    quantidade = Column(Integer)
    valor = Column(Float(4.2))
    data_cadastro = Column(DateTime, default=datetime.now)

    def __init__(self, nome:str, quantidade:int, valor:float, data_cadastro:Union[DateTime, None] = None):
        """
        Cria um Produto

        Arguments:
            nome: nome do produto
            quantidade: quantidade que se espera cadastrar
            valor: valor do produto
            data_cadastro: data em que o produto foi cadastrado
        """
        self.nome = nome
        self.quantidade = quantidade
        self.valor = valor

        # Se não for informado uma data, a mesma sera preenchida com a data atual no momento do cadastro
        if data_cadastro:
            self.data_cadastro = data_cadastro