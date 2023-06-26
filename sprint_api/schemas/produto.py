from pydantic import BaseModel
from typing import Optional, List
from model.produto import Produto

class ProdutoSchema(BaseModel):
    """
    Define como um novo produto a ser inserido deve ser apresentado
    """

    nome: str = "TV LG UHD"
    quantidade: Optional[int] = 12
    valor: float = 2950.99

class ProdutoBuscaSchema(BaseModel):
    """
    Define como deve ser a estrutura que representa a busca.
    Que será feita com base no id do produto.
    """

    id: int = 1

class ProdutoBuscaDelSchema(BaseModel):
    """
    Define como deve ser a estrutura que representa a busca para deletar.
    Que será feita com base no nome do produto.
    """

    nome: str = "TV LG UHD"

class ListagemProdutosSchema(BaseModel):
    """
    Define como uma listagem de produtos será retornada
    """

    produtos:List[ProdutoSchema]

def apresenta_produtos(produtos: List[Produto]):
    """
    Retorna uma representação dos produtos seguindo o schema definido em ProdutoViewSchema
    """
    result = []
    for produto in produtos:
        result.append({
            "nome": produto.nome,
            "quantidade": produto.quantidade,
            "valor": produto.valor
        })

    return {"produtos": result}

class ProdutoViewSchema(BaseModel):
    """
    Define como um produto será retornado
    """

    id: int = 1
    nome: str = "TV LG UHD"
    quantidade: Optional[int] = 12
    valor: float = 2950.99

class ProdutoDelSchema(BaseModel):
    """
    Define como deve ser a estrutura do dado retornado após uma requisição de remoção
    """

    mesage: str
    nome: str

def apresenta_produto(produto: Produto):
    """
    Retorna uma representação do produto seguindo o schema definido em ProdutoViewSchema
    """

    return {
        "id": produto.id,
        "nome": produto.nome,
        "quantidade": produto.quantidade,
        "valor": produto.valor
    }