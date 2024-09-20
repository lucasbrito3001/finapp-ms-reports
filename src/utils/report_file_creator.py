import pandas as pd
import xlsxwriter
import os

import xlsxwriter.utility
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet


class ReportColumn:
    key: str
    format: str
    width: int


class ReportFileCreator:
    def __init__(self, xlsx_creator, dataframe_creator):
        return
    
    formats_dict = {
        "currency": {"num_format": "[$R$] #,##0.00"},
        "datetime": {"num_format": "d/m/yyyy hh:mm"},
        "number": None,
        "text": None,
    }
    
    def applyWorksheetReportTemplate(self, workbook: Workbook, worksheet: Worksheet, total_cols: int):
        header_format = workbook.add_format({"bg_color": "green", "color": "white"})
        
        worksheet.conditional_format(
            f"A1:{xlsxwriter.utility.xl_col_to_name(total_cols - 1)}1",
            {"type": "no_errors", "format": header_format},
        )
        
        return
    
    def setWorksheetReportColumns(self, columns: list[ReportColumn], workbook: Workbook, worksheet: Worksheet):
        cell_formats_dict = {
            "currency": workbook.add_format({"num_format": "[$R$] #,##0.00"}),
            "datetime": workbook.add_format({"num_format": "d/m/yyyy hh:mm"}),
            "number": None,
            "text": None,
        }
        
        for idx, col in enumerate(columns):
            worksheet.set_column(
                first_col=idx,
                last_col=idx,
                width=col["width"],
                cell_format=cell_formats_dict[col["format"]],
            )
        
        return
    
    def fillWorksheet(self, dataframe: pd.DataFrame, worksheet: Worksheet):
        worksheet.write_row(0, 0, dataframe.columns)

        for row_num, values in enumerate(dataframe.values):
            worksheet.write_row(row_num + 1, 0, values)
            
        return

    def createXlsx(
        self,
        content,
        columns: list[ReportColumn],
        file_name: str,
        sheet_name: str,
    ) -> str:
        file_path = f'{os.environ.get("REPORTS_BASE_DIR")}/{file_name}.xlsx'
        
        workbook = xlsxwriter.workbook.Workbook(file_path)
        worksheet = workbook.add_worksheet(sheet_name)
        
        self.setWorksheetReportColumns(columns, workbook, worksheet)
        
        columns_keys = [column["key"] for column in columns]
        df = pd.DataFrame(content, columns=columns_keys, index=None)
        
        self.fillWorksheet(df, worksheet)
        
        self.applyWorksheetReportTemplate(workbook, worksheet, len(columns_keys))

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
