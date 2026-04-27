from enum import StrEnum


class MessageKey(StrEnum):
    CATEGORY_CREATED = "category.created"
    CATEGORY_UPDATED = "category.updated"
    CATEGORY_RETRIEVED = "category.retrieved"
    CATEGORY_LISTED = "category.listed"

    TICKET_CREATED = "ticket.created"
    TICKET_UPDATED = "ticket.updated"
    TICKET_RETRIEVED = "ticket.retrieved"
    TICKET_LISTED = "ticket.listed"

    COMMENT_CREATED = "comment.created"
    COMMENT_UPDATED = "comment.updated"
    COMMENT_RETRIEVED = "comment.retrieved"
    COMMENT_LISTED = "comment.listed"


MESSAGE_CATALOG: dict[str, dict[MessageKey, str]] = {
    "pt-BR": {
        MessageKey.CATEGORY_CREATED: "Categoria criada com sucesso",
        MessageKey.CATEGORY_UPDATED: "Categoria atualizada com sucesso",
        MessageKey.CATEGORY_UPDATED: "Categoria atualizada com sucesso",
        MessageKey.CATEGORY_RETRIEVED: "Categoria obtida com sucesso",
        MessageKey.CATEGORY_LISTED: "Categorias listadas com sucesso",
        MessageKey.TICKET_CREATED: "Ticket criado com sucesso",
        MessageKey.TICKET_UPDATED: "Ticket atualizado com sucesso",
        MessageKey.TICKET_RETRIEVED: "Ticket obtido com sucesso",
        MessageKey.TICKET_LISTED: "Tickets listados com sucesso",
        MessageKey.COMMENT_CREATED: "Comentário criado com sucesso",
        MessageKey.COMMENT_UPDATED: "Comentário atualizado com sucesso",
        MessageKey.COMMENT_RETRIEVED: "Comentário obtido com sucesso",
        MessageKey.COMMENT_LISTED: "Comentários listados com sucesso",
    }
}


def get_message(message_key: MessageKey, locale: str = "pt-BR") -> str:
    return MESSAGE_CATALOG[locale][message_key]
