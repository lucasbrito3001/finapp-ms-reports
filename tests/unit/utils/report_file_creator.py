import os
import unittest
from src.utils.report_file_creator import ReportFileCreator

report_file_creator = ReportFileCreator()

class TestStringMethods(unittest.TestCase):
    
    def test_creating_xlsx_sucessfully(self):
        reports_base_dir = "/tmp"
        os.environ["REPORTS_BASE_DIR"] = reports_base_dir
        
        file_name = "file"
        sheet_name = "sheet"
        report_content = [
            {"col1": "1", "col2": "2", "col3": "3"}, 
            {"col1": "2", "col2": "2", "col3": "3"}, 
            {"col1": "3", "col2": "2", "col3": "3"},
        ]
        report_columns = [
            {"key": "col1", "format": "number", "width": 10},
            {"key": "col2", "format": "text", "width": 10},
            {"key": "col3", "format": "currency", "width": 40}
        ]
        
        created_file_path = report_file_creator.createXlsx(report_content, report_columns, file_name, sheet_name)
        
        self.assertEqual(created_file_path, f'{reports_base_dir}/{file_name}.xlsx')

if __name__ == '__main__':
    unittest.main()