from app.domain.entities.category import Category


class CategoryDatabase:
    def __init__(self) -> None:
        self.id_counter = 0
        self.categories: list[Category] = []

    def add(self, category: Category) -> Category:
        self.categories.append(category)
        return category


category_db = CategoryDatabase()
