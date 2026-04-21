from app.domain.exceptions.base_exceptions import BusinessValidationError, NotFoundError


class TicketNotFoundError(NotFoundError):
    def __init__(self, ticket_id: int) -> None:
        super().__init__(resource_name="Ticket", resource_id=ticket_id)


class ClosedTicketUpdateError(BusinessValidationError):
    def __init__(self) -> None:
        message = "Um ticket encerrado não pode ser alterado."
        super().__init__(message=message)


class InvalidTicketTransitionError(BusinessValidationError):
    def __init__(self) -> None:
        message = "Transição de status inválida para o ticket."
        super().__init__(message=message)
