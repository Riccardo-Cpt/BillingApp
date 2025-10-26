import os
import json
import pdfplumber
import re
import pdfplumber
import re
import pandas as pd

class tables_excluded:
    _energy_provenience = {
        "fonti rinnovabili", "carbone", "gas naturale",
        "prodotti petroliferi", "nucleare"
    }
    _electricity_time_bands = {"f1", "f2", "f3"}

    @staticmethod
    def energy_provenience():
        return tables_excluded._energy_provenience

    @staticmethod
    def electricity_time_bands():
        return tables_excluded._electricity_time_bands


class process_pdf(tables_excluded):

    def __init__(self):
        self.supply_data = pd.DataFrame(columns=[
                        "INDIRIZZO",
                        "POD",
                        "POTENZA IMPEGNATA",
                        "POTENZA DISPONIBILE",
                        "TIPOLOGIA OFFERTA",
                        "INIZIO OFFERTA",
                        "FINE OFFERTA"
                    ])
        
        
        


    def remove_glyphs(self, text):
        """Remove glyphs like (cid:76) or (cid:<76>) from a text string."""
        # Match "(cid:" then optional "<", digits, optional ">", then ")"
        pattern = r'\(cid:<?\d+>?\)'
        return re.sub(pattern, '', text)

    def is_empty_cell(self, cell):
        """Check if a cell is empty (handles None and strings)."""
        return (cell or "").strip() == ""

    def is_empty_table(self, table_dict):
        """Check if a table is empty (all headers and rows are empty)."""
        return all(self.is_empty_cell(cell) for cell in table_dict["header"]) and \
               all(all(self.is_empty_cell(cell) for cell in row) for row in table_dict["rows"])

    def convert_table_to_text(self, table):
        table_text = " ".join(
                str(cell).lower() for row in table for cell in row if cell is not None
        )
        return table_text
    # Check if any keyword is present in the table

    def evaluate_table_text(self, table_text, keywords_to_discard):
        should_discard = any(
                keyword in table_text for keyword in keywords_to_discard
        )

        return should_discard

    def extract_tables_from_page(self, page, list_tables):
        tables = page.extract_tables()
        if tables:
            for table in tables:
                extracted_text = self.convert_table_to_text(table)
                if extracted_text and not self.evaluate_table_text(extracted_text, self.energy_provenience()):
                    list_tables.append(extracted_text)
        return list_tables


    def extract_text_and_tables(self, input_file_path, list_text, list_tables):
        with pdfplumber.open(input_file_path) as doc:
            for page in doc.pages:
                # Extract tables once
                tables = page.extract_tables()
                list_tables = self.extract_tables_from_page(page, list_tables)
                # Extract text
                text = page.extract_text()
                list_text.append(text)
        return list_text, list_tables


