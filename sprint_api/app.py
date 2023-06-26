from flask import redirect
from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS
from schemas import *
from model import Session, Produto
from logger import logger
from sqlalchemy.exc import IntegrityError
from urllib.parse import unquote


info = Info(title="Sprint API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo as tags para documentação
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
produto_tag = Tag(name="Produto", description="Adição, visualização e remoção de produtos à base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/produto', tags=[produto_tag], responses={"200": ProdutoViewSchema, "409": ErrorSchema, "400": ErrorSchema})

def add_produto(form: ProdutoSchema):
    """
    Adiciona um novo produto a base de dados
    Retorna uma representação dos produtos adicionados
    """

    produto = Produto(
        nome=form.nome,
        quantidade=form.quantidade,
        valor=form.valor)
    logger.debug(f"Adicionado produto de nome: '{produto.nome}'")
    try:
        # Criando conexão com a base de dados
        session = Session()
        
        # Adicionando o produto
        session.add(produto)

        # Efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado produto de nome: '{produto.nome}'")

        return apresenta_produto(produto), 200
    
    except IntegrityError as e:
        # Como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Produto de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
        return {"mesage": error_msg}, 409
    
    except Exception as e:
        # Como um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
        return {"mesage": error_msg}, 400
    

@app.get('/produtos', tags=[produto_tag], responses={"200": ListagemProdutosSchema, "404": ErrorSchema})

def get_produtos():
    """
    Faz a busca por todos os produtos cadastrados e retorna uma representação da listagem de produtos.
    """

    logger.debug(f"Coletando produtos")
    # Criando conexão com o banco de dados
    session = Session()
    # Fazebo a busca
    produtos = session.query(Produto).all()

    if not produtos:
        # Se não há produtos cadastrados
        return {"produtos": []}, 200
    else:
        logger.debug(f"%d produtos encontrados" % len(produtos))
        # Retorna a representação de produtos
        print(produtos)
        return apresenta_produtos(produtos), 200

   
@app.get('/produto', tags=[produto_tag], responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def get_produto(query: ProdutoBuscaSchema):
    """
    Faz a busca por um Produto a partir do id do produto retorna uma representação dos produtos e comentários associados.
    """
    produto_id = query.id
    logger.debug(f"Coletando dados sobre produto #{produto_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produto = session.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao buscar produto '{produto_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Produto econtrado: '{produto.nome}'")
        # retorna a representação de produto
        return apresenta_produto(produto), 200


@app.delete('/produto', tags=[produto_tag],
            responses={"200": ProdutoDelSchema, "404": ErrorSchema})
def del_produto(query: ProdutoBuscaDelSchema):
    """Deleta um Produto a partir do nome de produto informado

    Retorna uma mensagem de confirmação da remoção.
    """
    produto_nome = unquote(unquote(query.nome))
    print(produto_nome)
    logger.debug(f"Deletando dados sobre produto #{produto_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Produto).filter(Produto.nome == produto_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado produto #{produto_nome}")
        return {"mesage": "Produto removido", "Nome": produto_nome}
    else:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao deletar produto #'{produto_nome}', {error_msg}")
        return {"mesage": error_msg}, 404