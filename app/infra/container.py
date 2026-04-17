from dependency_injector import containers, providers

from app.application.use_cases.category.create_category import CreateCategoryUseCase
from app.application.use_cases.category.get_category_by_id import GetCategoryByIdUseCase
from app.application.use_cases.category.list_categories import ListCategoriesUseCase
from app.application.use_cases.category.update_category import UpdateCategoryUseCase
from app.application.use_cases.ticket.create_ticket import CreateTicketUseCase
from app.application.use_cases.ticket.get_ticket_by_id import GetTicketByIdUseCase
from app.application.use_cases.ticket.list_tickets import ListTicketsUseCase
from app.application.use_cases.ticket.update_ticket import UpdateTicketUseCase
from app.infra.db.repositories.category_repository import InMemoryCategoryRepository
from app.infra.db.repositories.ticket_repository import InMemoryTicketRepository


class Container(containers.DeclarativeContainer):
    # 1. Configuração de fiação (Wiring)
    # Isso diz ao container quais arquivos usarão o @inject
    # Normalmente apontamos para os módulos de rotas
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.adapters.http.routers.ticket_router",
            "app.adapters.http.routers.category_router",
        ]
    )

    # 2. Providers de Infraestrutura
    # Usamos Singleton para o repositório em memória, pois queremos que todos
    # os Use Cases acessem a mesma "lista" de tickets.
    ticket_repo = providers.Singleton(InMemoryTicketRepository)
    category_repo = providers.Singleton(InMemoryCategoryRepository)

    # 3. Providers de Application (Use Cases)
    # Usamos Factory para criar uma nova instância do Use Case a cada requisição
    create_ticket_use_case = providers.Factory(
        CreateTicketUseCase,
        ticket_repo=ticket_repo,  # Aqui injetamos o repositório definido acima
        category_repo=category_repo,
    )

    update_ticket_use_case = providers.Factory(
        UpdateTicketUseCase, ticket_repo=ticket_repo, category_repo=category_repo
    )

    list_tickets_use_case = providers.Factory(ListTicketsUseCase, repo=ticket_repo)

    get_ticket_by_id_use_case = providers.Factory(
        GetTicketByIdUseCase, repo=ticket_repo
    )

    create_category_use_case = providers.Factory(
        CreateCategoryUseCase, repo=category_repo
    )

    update_category_use_case = providers.Factory(
        UpdateCategoryUseCase, repo=category_repo
    )

    list_categories_use_case = providers.Factory(
        ListCategoriesUseCase, repo=category_repo
    )

    get_category_by_id_use_case = providers.Factory(
        GetCategoryByIdUseCase, repo=category_repo
    )
