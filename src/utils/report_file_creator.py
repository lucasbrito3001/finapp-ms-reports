import pandas as pd
import xlsxwriter
import os

import xlsxwriter.utility


class ReportColumn:
    key: str
    format: str
    width: int


class ReportFileCreator:
    formats_dict = {
        "currency": {"num_format": "[$R$] #,##0.00"},
        "datetime": {"num_format": "d/m/yyyy hh:mm"},
        "number": None,
        "text": None,
    }

    def createXlsx(
        self,
        content,
        columns: list[ReportColumn],
        index: bool,
        file_name: str,
        sheet_name: str,
    ) -> str:
        file_path = f'{os.environ.get("REPORTS_BASE_DIR")}/{file_name}.xlsx'

        columns_keys = [column["key"] for column in columns]

        df = pd.DataFrame(content, columns=columns_keys, index=None)

        workbook = xlsxwriter.workbook.Workbook(file_path)
        worksheet = workbook.add_worksheet(sheet_name)

        for idx, col in enumerate(columns):
            worksheet.set_column(
                first_col=idx,
                last_col=idx,
                width=col["width"],
                cell_format=workbook.add_format(self.formats_dict[col["format"]]),
            )

        header_format = workbook.add_format({"bg_color": "green", "color": "white"})

        worksheet.write_row(0, 0, df.columns)

        for row_num, values in enumerate(df.values):
            worksheet.write_row(row_num + 1, 0, values)

        worksheet.conditional_format(
            f"A1:{xlsxwriter.utility.xl_col_to_name(len(columns) - 1)}1",
            {"type": "no_errors", "format": header_format},
        )

        workbook.close()

        return file_path

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
