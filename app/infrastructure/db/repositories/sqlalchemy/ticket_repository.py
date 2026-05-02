from math import ceil
from typing import Any

from app.application.dtos.pagination import PagedResult, PaginationParams
from app.application.dtos.sorting import SortDirection
from app.application.dtos.ticket_query import TicketFilter
from app.application.interfaces.repositories.ticket_repository import ITicketRepository
from app.domain.entities.ticket import Ticket
from app.domain.enum.ticket_priority import TicketPriority
from app.domain.enum.ticket_sort_field import TicketSortField
from app.domain.enum.ticket_status import TicketStatus
from app.domain.exceptions.ticket_exceptions import TicketNotFoundError
from app.infrastructure.db.sqlalchemy.models import TicketORM
from sqlalchemy import Case, case
from sqlalchemy.orm import InstrumentedAttribute, Query, Session


class SQLAlchemyTicketRepository(ITicketRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    # ========== Contract methods ==========
    def create(self, ticket: Ticket) -> Ticket:

        if not ticket:
            raise ValueError("Ticket cannot be None")

        ticket_orm = TicketORM(
            title=ticket.title,
            description=ticket.description,
            status=ticket.status,
            priority=ticket.priority,
            category_id=ticket.category_id,
        )

        self._session.add(ticket_orm)
        self._session.commit()
        self._session.refresh(ticket_orm)

        return self._orm_to_domain(ticket_orm)

    def update(self, updated_ticket: Ticket) -> Ticket:

        if not updated_ticket.id or updated_ticket.id <= 0:
            raise ValueError("Ticket must have a valid ID")

        ticket_orm = self._get_ticket_orm_by_id(updated_ticket.id)

        ticket_orm.category_id = updated_ticket.category_id
        ticket_orm.status = updated_ticket.status
        ticket_orm.priority = updated_ticket.priority

        self._session.commit()
        self._session.refresh(ticket_orm)

        return self._orm_to_domain(ticket_orm)

    def list_by_filter(
        self, ticket_filter: TicketFilter, pagination_params: PaginationParams
    ) -> PagedResult[Ticket]:

        query = self._session.query(TicketORM)

        # Aplicar filtros (SQL WHERE)
        query = self._apply_filters(ticket_filter, query)

        query = self._apply_sorting(ticket_filter, query)

        return self._paginate(pagination_params, query)

    def get_by_id(self, ticket_id: int) -> Ticket:
        ticket_orm = self._get_ticket_orm_by_id(ticket_id)

        return self._orm_to_domain(ticket_orm)

    # ========== Private methods ==========
    def _get_ticket_orm_by_id(self, ticket_id: int) -> TicketORM:
        ticket_orm = self._session.get(TicketORM, ticket_id)

        if ticket_orm is None:
            raise TicketNotFoundError(ticket_id)

        return ticket_orm

    def _orm_to_domain(self, ticket_orm: TicketORM) -> Ticket:
        return Ticket(
            id=ticket_orm.id,
            title=ticket_orm.title,
            description=ticket_orm.description,
            status=ticket_orm.status,
            priority=ticket_orm.priority,
            category_id=ticket_orm.category_id,
            created_at=ticket_orm.created_at,
            updated_at=ticket_orm.updated_at,
        )

    def _apply_filters(
        self, ticket_filter: TicketFilter, query: Query[TicketORM]
    ) -> Query[TicketORM]:
        if ticket_filter.status:
            query = query.filter(TicketORM.status == ticket_filter.status)
        if ticket_filter.priority:
            query = query.filter(TicketORM.priority == ticket_filter.priority)
        if ticket_filter.category_id:
            query = query.filter(TicketORM.category_id == ticket_filter.category_id)

        return query

    def _apply_sorting(
        self, ticket_filter: TicketFilter, query: Query[TicketORM]
    ) -> Query[TicketORM]:

        ORDER_FIELDS: dict[TicketSortField, InstrumentedAttribute[Any] | Case[Any]] = {
            TicketSortField.ID: TicketORM.id,
            TicketSortField.TITLE: TicketORM.title,
            TicketSortField.PRIORITY: self._priority_order_expression(),
            TicketSortField.STATUS: self._status_order_expression(),
        }

        sort_column = ORDER_FIELDS[ticket_filter.sort_field]

        if ticket_filter.sort_direction == SortDirection.ASC:
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        return query

    def _priority_order_expression(self) -> Case[Any]:
        priority_order = case(
            {priority: priority.sort_order for priority in TicketPriority},
            value=TicketORM.priority,
        )

        return priority_order

    def _status_order_expression(self) -> Case[Any]:
        status_order = case(
            {status: status.sort_order for status in TicketStatus},
            value=TicketORM.status,
        )

        return status_order

    def _paginate(
        self, pagination_params: PaginationParams, query: Query[TicketORM]
    ) -> PagedResult[Ticket]:
        total_items = query.count()

        paginated_tickets_orm = (
            query.offset(pagination_params.offset)
            .limit(pagination_params.page_size)
            .all()
        )

        total_pages = (
            ceil(total_items / pagination_params.page_size) if total_items else 0
        )

        tickets = [
            self._orm_to_domain(ticket_orm) for ticket_orm in paginated_tickets_orm
        ]

        return PagedResult(
            items=tickets,
            total_items=total_items,
            page=pagination_params.page,
            page_size=pagination_params.page_size,
            total_pages=total_pages,
        )
