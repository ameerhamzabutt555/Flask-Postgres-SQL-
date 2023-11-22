import tabula
import pandas as pd
import re


def extract_data_from_pdf_one(pdf_path):
    final_rows=[]
    final_result_table = pd.DataFrame()
    # Strings to find
    strings_to_find = ["IAS 1.82(a)", "IAS 1.82(ba)", "IAS 1.82(d)", "IAS 1.81B(a)(ii)", "IFRS 12.B10(b)", "IAS 1.78(b)", "IAS 1.54(g)", "IAS 1.54(i)", "IAS 1.54(m)", "IAS 1.55"]
    # Read the tables from the PDF and get the page numbers
    tables = tabula.read_pdf(pdf_path, pages="all")
    # Iterate through the tables
    # Define columns
    column_counts = {}
    for table_number, table in enumerate(tables, start=1):
        df = pd.DataFrame(table)
        for index, row in df.iterrows():
            # Check if any of the strings are in any cell of the row
            found_strings_in_row = [string for string in strings_to_find if any(isinstance(cell, str) and string in cell for cell in row) or row[0] == "Operating profit"]
            # If any new strings are found, apply regex operations to each element in the row
            if found_strings_in_row:
                # Apply regex operations to each element in the row only if the specific string is found
                for string_to_find in found_strings_in_row:
                    pattern = f'(^|\s){re.escape(string_to_find)}(\s|$)'
                    row = [re.sub(pattern, ' ', str(cell)) for cell in row]
                # Remove empty strings (' ') from the resulting row
                row = list(filter(lambda x: x != ' ', row))
                # Extract specific elements from the row (e.g., values at index 0, 2, and 3)
                extracted_values = [re.sub(r'\(|\)', '', value) for value in [row[0], row[2], row[3]]]
                final_rows.append(extracted_values)
        
        # Filter out columns with names like 'Unnamed: 0', 'Unnamed: 1', etc.
        valid_columns = [column for column in df.columns if not column.startswith('Unnamed')]
        # Count occurrences of each valid column name
        for column in valid_columns:
            if column in column_counts:
                column_counts[column] += 1
            else:
                column_counts[column] = 1

    # Find the two most frequently occurring valid column names
    most_used_columns = sorted(column_counts, key=column_counts.get, reverse=True)[:2]
    most_used_columns.insert(0, "Name")
    final_result_table[most_used_columns] = pd.DataFrame(columns=most_used_columns)

    for row in final_rows:
        row[0] = re.sub(r'^–', '', str(row[0]))
        final_result_table = final_result_table._append(pd.Series(row, index=final_result_table.columns), ignore_index=True)
        # Remove leading and trailing whitespace from the 'Name' column
        final_result_table['Name'] = final_result_table['Name'].str.strip()
        # Drop duplicates based on the 'Name' column
        final_result_table = final_result_table.drop_duplicates(subset='Name', keep='first')



    columns_to_display = final_result_table.columns

    # Initialize an empty list to store selected rows
    selected_rows = []
    rows=[]

    # Iterate through the DataFrame and select rows
    for index, row in final_result_table.iterrows():
        selected_row = final_result_table.loc[index, columns_to_display]
        selected_rows.append(selected_row)

    # Display the selected rows
    for row in selected_rows:
        rows.append(row)
    return rows


