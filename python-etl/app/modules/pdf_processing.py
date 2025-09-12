import os
import json
import pdfplumber
import re
import pdfplumber
import re

class process_pdf:

    def __init__(self):
        pass

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
        """Extract non-empty tables from a single page."""
        tables = page.extract_tables()
        if tables:
            for table in tables:
                #exclude tables giving information about energy provenience
                extracted_text = self.convert_table_to_text(table=table)
                fl_provenience = self.evaluate_table_text(extracted_text, tables_excluded.energy_provenience())
                #fl_time_bands = self.evaluate_table_text(extracted_text, tables_excluded.electricity_time_bands())
                if (table and not fl_provenience):# or (table and not fl_time_bands):
                    if extracted_text != "":
                        extracted_cleaned_text = extracted_text.lower().replace("none", "").replace("\n", " ")
                        list_tables.append(extracted_cleaned_text)

        return list_tables

    def extract_text_and_tables(self, input_file_path, list_text, list_tables):
        with pdfplumber.open(input_file_path) as doc:
            for page_num, page in enumerate(doc.pages, start=1):
                # Extract tables first
                tables = page.extract_tables()
                list_tables = self.extract_tables_from_page(page, list_tables)

                #extract whole text from table
                text = page.extract_text()
                list_text.append(text)

            return list_text, list_tables


class tables_excluded:
    def energy_provenience():
        irrelevant_keywords = {
        "fonti rinnovabili", "carbone", "gas naturale",
        "prodotti petroliferi", "nucleare"
        }
        return irrelevant_keywords
    
    def electricity_time_bands():
        time_bands = {
        "f1", "f2", "f3"
        }
        return time_bands


class tables_excluded:
    def energy_provenience():
        irrelevant_keywords = {
        "fonti rinnovabili", "carbone", "gas naturale",
        "prodotti petroliferi", "nucleare"
        }
        return irrelevant_keywords
    
    def electricity_time_bands():
        time_bands = {
        "f1", "f2", "f3"
        }
        return time_bands