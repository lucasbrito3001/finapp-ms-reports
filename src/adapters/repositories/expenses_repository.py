class ExpensesRepository:
    expenses = [{"name": "Lucas", "age": 24}, {"name": "Bianca", "age": 23}]

    def getExpensesByFilters(self, filters: dict[str, any]) -> None | list[any]:
        return self.expenses
