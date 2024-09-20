import xlsxwriter
from xlsxwriter.workbook import Workbook as XlsxWriterWorkbook
from xlsxwriter.worksheet import Worksheet as XlsxWriterWorksheet
import pandas as pd

    
class Worksheet:
    def __init__(self, external_worksheet: XlsxWriterWorksheet):
        self.external_worksheet = external_worksheet
        return
    
    def conditionalFormat(self, first_row: int, last_row: int, last_col: int):
        self.external_worksheet.conditional_format()
        return
    
class Workbook:
    def __init__(self, external_workbook: XlsxWriterWorkbook):
        self.external_workbook = external_workbook
        return
    
    def addWorksheet(self, name: str) -> Worksheet:
        external_worksheet = self.external_workbook.add_worksheet(name)
        
        return Worksheet(external_worksheet)

class XlsxCreator:
    def createDataFrame(self, content: any, columns: any):
        return pd.DataFrame(data=content, columns=columns)
        
    def createWorkbook(self, filename: str) -> Workbook:
        external_workbook = xlsxwriter.workbook.Workbook(filename)
        
        return Workbook(external_workbook)