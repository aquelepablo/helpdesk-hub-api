# Project Structure

O projeto segue uma organizacao em camadas, com separacao entre entrega HTTP, casos de uso, dominio e detalhes tecnicos de infraestrutura.

```text
app/
  api/
    docs/
    exception_handlers/
    mappers/
    messages/
    routers/
    schemas/

  application/
    bootstrap/
    dtos/
    interfaces/
      repositories/
    use_cases/
      category/
      comment/
      ticket/

  domain/
    entities/
    enum/
    exceptions/

  infrastructure/
    bootstrap/
    db/
      repositories/
        memory/
        sqlalchemy/
      sqlalchemy/
        models/
    logging/
    settings/
    container.py

  main.py

tests/
  integration/
  unit/
```

## `app/api`

Camada HTTP da aplicacao.

Responsabilidades:

- definir routers FastAPI
- validar request/response com schemas Pydantic
- mapear DTOs de entrada e saida
- registrar exception handlers e formatos padrao de erro
- expor mensagens e contratos da API

Nao deve concentrar regra de negocio.

## `app/application`

Camada de orquestracao dos casos de uso.

Responsabilidades:

- implementar fluxos de negocio orientados a caso de uso
- definir DTOs de entrada, saida, paginacao e filtros
- depender de contratos de repository, nao de implementacoes concretas
- manter a regra de aplicacao isolada de FastAPI e SQLAlchemy

Subpastas relevantes:

- `dtos/`: filtros, ordenacao e paginacao
- `interfaces/repositories/`: contratos usados pelos casos de uso
- `use_cases/category/`: fluxos de categoria
- `use_cases/ticket/`: fluxos de ticket
- `use_cases/comment/`: fluxos de comentario
- `bootstrap/default_categories.py`: categorias padrao usadas no seed

## `app/domain`

Nucleo do dominio.

Responsabilidades:

- representar entidades como `Category`, `Ticket` e `Comment`
- definir enums de negocio, como prioridade, status e campo de ordenacao
- centralizar excecoes de dominio

Essa camada nao deve depender de FastAPI, SQLAlchemy ou detalhes de infraestrutura.

## `app/infrastructure`

Camada tecnica da aplicacao.

Responsabilidades:

- carregar configuracoes e variaveis de ambiente
- configurar logging
- compor dependencias no container
- implementar persistencia concreta
- executar bootstrap tecnico, como seed inicial

### Persistencia

O projeto possui duas familias de repository:

- `db/repositories/sqlalchemy/`: implementacao atualmente usada pela aplicacao
- `db/repositories/memory/`: implementacao em memoria mantida como apoio historico e referencia de comportamento

Em `db/sqlalchemy/` ficam:

- `database.py`: engine, session factory e `get_db_session`
- `models/`: models ORM de `categories`, `tickets` e `comments`

### Bootstrap

`bootstrap/seed_categories.py` popula categorias padrao no startup, evitando recriacao de registros ja existentes.

## `app/main.py`

Ponto principal da aplicacao FastAPI.

Responsabilidades:

- criar a aplicacao
- registrar routers e exception handlers
- configurar o container
- executar seed no lifespan
- criar as tabelas do banco no startup

## `tests`

O projeto separa testes por nivel:

- `tests/integration/`: cobre endpoints, startup e acesso ao banco
- `tests/unit/`: cobre schemas e configuracoes

Atualmente a suite valida:

- contratos HTTP principais
- filtros, paginacao e ordenacao de tickets
- fluxo de categorias e comentarios
- leitura de settings via `.env`
- criacao de sessao SQLAlchemy

## Fluxo resumido

O fluxo principal segue este caminho:

1. router recebe a requisicao HTTP
2. schema valida os dados
3. router monta o input do caso de uso
4. use case executa a regra e depende de interfaces
5. repository concreto persiste ou consulta no banco
6. mapper/schema formata a resposta HTTP

## Observacoes

- A organizacao e inspirada em Clean Architecture, mas aplicada de forma pragmatica.
- Nem toda pasta representa uma fronteira rigida; o objetivo aqui e manter responsabilidades claras e facilitar evolucao incremental.
- A presenca simultanea de repositories em memoria e SQLAlchemy reflete a transicao do projeto da fase inicial para persistencia real.
