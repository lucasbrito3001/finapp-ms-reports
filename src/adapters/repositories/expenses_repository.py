import json
from src.infra.database import DatabaseConnection


class ExpensesRepository:
    def __init__(self, database_connection: DatabaseConnection) -> None:
        self.database_connection = database_connection
        pass

    expenses = [{"name": "Lucas", "age": 24}, {"name": "Bianca", "age": 23}]

    def getExpensesByMonth(
        self, target_month: int, target_year: int
    ) -> None | list[any]:
        cursor = self.database_connection.create_cursor()

        result = cursor.run_dql_query(
            "SELECT * FROM expenses WHERE month = %s AND year = %s",
            (
                target_month,
                target_year,
            ),
        )

        return result
