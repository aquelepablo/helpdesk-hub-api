from dependency_injector import containers, providers

from app.application.use_cases.category.create_category import CreateCategoryUseCase
from app.application.use_cases.category.get_category_by_id import GetCategoryByIdUseCase
from app.application.use_cases.category.list_categories import ListCategoriesUseCase
from app.application.use_cases.category.update_category import UpdateCategoryUseCase
from app.application.use_cases.comment.create_comment import CreateCommentUseCase
from app.application.use_cases.comment.list_comments import ListCommentsUseCase
from app.application.use_cases.comment.update_comment import UpdateCommentUseCase
from app.application.use_cases.ticket.create_ticket import CreateTicketUseCase
from app.application.use_cases.ticket.get_ticket_by_id import GetTicketByIdUseCase
from app.application.use_cases.ticket.list_tickets import ListTicketsUseCase
from app.application.use_cases.ticket.update_ticket import UpdateTicketUseCase
from app.infrastructure.db.repositories.memory.category_repository import (
    InMemoryCategoryRepository,
)
from app.infrastructure.db.repositories.memory.comment_repository import (
    InMemoryCommentRepository,
)
from app.infrastructure.db.repositories.memory.ticket_repository import (
    InMemoryTicketRepository,
)


class Container(containers.DeclarativeContainer):
    """
    Container de dependências para a aplicação.
    """

    ticket_repository = providers.Singleton(InMemoryTicketRepository)
    category_repository = providers.Singleton(InMemoryCategoryRepository)
    comment_repository = providers.Singleton(InMemoryCommentRepository)

    # Categories
    create_category_use_case = providers.Factory(
        CreateCategoryUseCase, category_repository=category_repository
    )

    update_category_use_case = providers.Factory(
        UpdateCategoryUseCase, category_repository=category_repository
    )

    list_categories_use_case = providers.Factory(
        ListCategoriesUseCase, category_repository=category_repository
    )

    get_category_by_id_use_case = providers.Factory(
        GetCategoryByIdUseCase, category_repository=category_repository
    )

    # Tickets
    create_ticket_use_case = providers.Factory(
        CreateTicketUseCase,
        ticket_repository=ticket_repository,
        category_repository=category_repository,
    )

    update_ticket_use_case = providers.Factory(
        UpdateTicketUseCase,
        ticket_repository=ticket_repository,
        category_repository=category_repository,
    )

    list_tickets_use_case = providers.Factory(
        ListTicketsUseCase, ticket_repository=ticket_repository
    )

    get_ticket_by_id_use_case = providers.Factory(
        GetTicketByIdUseCase, ticket_repository=ticket_repository
    )

    # Comments
    create_comment_use_case = providers.Factory(
        CreateCommentUseCase,
        comment_repository=comment_repository,
        ticket_repository=ticket_repository,
    )

    update_comment_use_case = providers.Factory(
        UpdateCommentUseCase,
        comment_repository=comment_repository,
        ticket_repository=ticket_repository,
    )

    list_comments_use_case = providers.Factory(
        ListCommentsUseCase,
        comment_repository=comment_repository,
        ticket_repository=ticket_repository,
    )
