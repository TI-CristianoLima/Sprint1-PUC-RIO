from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# importando os modelos da base
from model.base import Base
from model.produto import Produto

db_path = "database/"
# Verifica se o diretorio não existe

if not os.path.exists(db_path):
    # então ele cria o diretorio
    os.makedirs(db_path)

db_url = 'sqlite:///%s/db.sqlite3' % db_path

# Cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)

# Cria o banco se ele não existir
if not database_exists(engine.url):
    create_database(engine.url)

# Cria as tabelas no banco caso não existam
Base.metadata.create_all(engine)