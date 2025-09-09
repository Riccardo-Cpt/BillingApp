import os
import json
import pdfplumber
import re

in_path = r"C:\Users\admin\Desktop\MieiProgetti\TestAI\illumia_bills"
out_path= os.path.join(in_path, "output_tables")
in_path_single = os.path.join(in_path, "412401445158.pdf")

class process_pdf:
    def remove_glyphs(text):
        """Remove glyphs like (cid:76) or (cid:<76>) from a text string."""
        # Match "(cid:" then optional "<", digits, optional ">", then ")"
        pattern = r'\(cid:<?\d+>?\)'
        return re.sub(pattern, '', text)

    def is_empty_cell(cell):
        """Check if a cell is empty (handles None and strings)."""
        return (cell or "").strip() == ""

    def is_empty_table(table_dict):
        """Check if a table is empty (all headers and rows are empty)."""
        return all(is_empty_cell(cell) for cell in table_dict["header"]) and \
               all(all(is_empty_cell(cell) for cell in row) for row in table_dict["rows"])

    def convert_table_to_text(table):
        table_text = " ".join(
                str(cell).lower() for row in table for cell in row if cell is not None
        )
        return table_text
    # Check if any keyword is present in the table

    def evaluate_table_text(table_text, keywords_to_discard):
        should_discard = any(
                keyword in table_text for keyword in keywords_to_discard
        )

        return should_discard

    def extract_tables_from_page(page, list_tables):
        """Extract non-empty tables from a single page."""
        tables = page.extract_tables()
        if tables:
            for table in tables:
                #exclude tables giving information about energy provenience
                extracted_text = convert_table_to_text(table=table)
                fl_provenience = evaluate_table_text(extracted_text, tables_excluded.energy_provenience())
                #fl_time_bands = evaluate_table_text(extracted_text, tables_excluded.electricity_time_bands())
                if (table and not fl_provenience):# or (table and not fl_time_bands):
                    if extracted_text != "":
                        extracted_cleaned_text = extracted_text.lower().replace("none", "").replace("\n", " ")
                        list_tables.append(extracted_cleaned_text)
                
                #if fl_time_bands==True:
                #    print(1)
                #    table_dict = {
                #        "header": table[0],
                #        "rows": table[1:]
                #    }
                #    #check if the table is not empty before extracting it
                #    if not is_empty_table(table_dict):
                #        json_str = json.dumps(table_dict, ensure_ascii=False, indent=2)
                #        list_tables.append(json_str)
        return list_tables

    def extract_text_and_tables(input_file_path, list_text, list_tables):
        with pdfplumber.open(in_file) as doc:
            for page_num, page in enumerate(doc.pages, start=1):
                # Extract tables first
                tables = page.extract_tables()
                list_tables = extract_tables_from_page(page, list_tables)

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