import pandas as pd
import os


class ReportFileCreator:
    def createXlsx(
        self,
        content,
        columns: None | list[str],
        index: bool,
        filename: str,
    ) -> str:
        filepath = f'{os.environ.get("REPORTS_BASE_DIR")}/{filename}.xlsx'

        df = pd.DataFrame(content, columns)

        df.to_excel(
            filepath,
            sheet_name=f"{filename}",
            index=index,
        )

        return filepath

    def createCsv(
        self,
        content,
        columns: None | list[str],
        index: bool,
        subdir: str,
        filename: str,
    ) -> None:
        df = pd.DataFrame(content, columns)

        df.to_csv(
            path_or_buf=f'{os.environ.get("REPORTS_BASE_DIR")}/{subdir}/{filename}.csv',
            index=index,
            sep=",",
        )
