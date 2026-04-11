from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(slots=True)
class Category:
    id: int = 0
    name: str = ""
    description: str = ""
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
