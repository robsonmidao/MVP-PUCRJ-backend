from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Estacionamento, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Controle de Estacionamento", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
estacionamento_tag = Tag(name="Estacionamento", description="Adição, visualização e remoção de registros de estacionamento à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um registro de estacionamento cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/estacionamento', tags=[estacionamento_tag],
          responses={"200": EstacionamentoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_estacionamento(form: EstacionamentoSchema):
    """Adiciona um novo registro de estacionamento à base de dados

    Retorna uma representação dos registros de estacionamento e comentários associados.
    """
    estacionamento = Estacionamento(
        placa=form.placa,
        veiculo=form.veiculo,
        data_hora_entrada=form.data_hora_entrada,
        data_hora_saida=form.data_hora_saida,
        valor=form.valor
        )
    logger.debug(f"Adicionando registro de estacionamento da placa: '{estacionamento.placa}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando registro de estacionamento
        session.add(estacionamento)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado registro de estacionamento da placa: '{estacionamento.placa}'")
        return apresenta_estacionamentos(estacionamento), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Registro de estacionamento de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar registro de estacionamento '{estacionamento.placa}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = e #"Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar registro de estacionamento '{estacionamento.id,estacionamento.placa,estacionamento.veiculo,estacionamento.data_hora_entrada,estacionamento.data_hora_saida,estacionamento.data_insercao,estacionamento.valor}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/estacionamentos', tags=[estacionamento_tag],
         responses={"200": ListagemEstacionamentoSchema, "404": ErrorSchema})
def get_estacionamentos():
    """Faz a busca por todos os registros de estacionamento cadastrados

    Retorna uma representação da listagem de registros de estacionamento.
    """
    logger.debug(f"Coletando registros de estacionamento ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    estacionamentos = session.query(Estacionamento).all()

    if not estacionamentos:
        # se não há estacionamentos cadastrados
        return {"estacionamentos": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(estacionamentos))
        # retorna a representação de registro de estacionamento
        print(estacionamentos)
        return apresenta_estacionamentos(estacionamentos), 200


@app.get('/estacionamento', tags=[estacionamento_tag],
         responses={"200": EstacionamentoViewSchema, "404": ErrorSchema})
def get_estacionamento(query: EstacionamentoBuscaSchema):
    """Faz a busca por um registro de estacionamento a partir do id do estacionamento

    Retorna uma representação dos registros de estacionamento e comentários associados.
    """
    estacionamento_id = query.id
    logger.debug(f"Coletando dados sobre estacionamento #{estacionamento_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a buscaPrata
    estacionamento = session.query(Estacionamento).filter(Estacionamento.id == estacionamento_id).first()

    if not estacionamento:
        # se o registro de estacionamento não foi encontrado
        error_msg = "Registro de estacionamento não encontrado na base :/"
        logger.warning(f"Erro ao buscar estacionamento '{estacionamento_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Registro de estacionamento econtrado: '{estacionamento.placa}'")
        # retorna a representação de registro de estacionamento
        return apresenta_estacionamento(estacionamento), 200


@app.delete('/estacionamento', tags=[estacionamento_tag],
            responses={"200": EstacionamentoDelSchema, "404": ErrorSchema})
def del_estacionamento(query: EstacionamentoBuscaSchema):
    """Deleta um registro de estacionamento a partir do id de estacionamento informado

    Retorna uma mensagem de confirmação da remoção.
    """
    estacionamento_id = query.id

    logger.debug(f"Deletando dados sobre registros de estacionamento #{estacionamento_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Estacionamento).filter(Estacionamento.id == estacionamento_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado registros de estacionamento #{estacionamento_id}")
        return {"mesage": "Registro de estacionamento removido", "id": estacionamento_id}
    else:
        # se o registro de estacionamento não foi encontrado
        error_msg = "Registro de estacionamento não encontrado na base :/"
        logger.warning(f"Erro ao deletar registro de estacionamento #'{estacionamento_id}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/comentario', tags=[comentario_tag],
          responses={"200": EstacionamentoViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adiciona um novo comentário à um registro de estacionamento cadastrado na base identificado pelo id

    Retorna uma representação dos registros de estacionamento e comentários associados.
    """
    estacionamento_id  = form.estacionamento_id
    logger.debug(f"Adicionando comentários ao registro de estacionamento #{estacionamento_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo registro de estacionamento
    estacionamento = session.query(Estacionamento).filter(Estacionamento.id == estacionamento_id).first()

    if not estacionamento:
        # se registro de estacionamento não encontrado
        error_msg = "Registro de estacionamento não encontrado na base :/"
        logger.warning(f"Erro ao adicionar comentário ao registro de estacionamento '{estacionamento_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # adicionando o comentário ao registro de estacionamento
    estacionamento.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário ao registro de estacionamento #{estacionamento_id}")

    # retorna a representação de registro de estacionamento
    return apresenta_estacionamento(estacionamento), 200
