import tabula
import pandas as pd




def extract_data_from_pdf_five(pdf_path):
    # Specify the page numbers you want to extract
    pages_to_extract = [3, 4]
    rows=[]
    # Read the tables from the PDF
    tables = tabula.read_pdf(pdf_path, pages=pages_to_extract, multiple_tables=True)
    # print(tables)
    # Iterate through the extracted tables
    for table in tables:
        # Create a DataFrame from the extracted table
        df = pd.DataFrame(table)

        # Rename the first column to "Name"
        df = df.rename(columns={df.columns[0]: "Name"})

        # Define columns to be dropped
        columns_to_drop = ['NOTA', 'Unnamed: 0', 'Unnamed: 1']

        # Drop the specified columns if they exist in the DataFrame
        columns_to_drop = [col for col in columns_to_drop if col in df.columns]
        if columns_to_drop:
            df = df.drop(columns=columns_to_drop)

        # Check if the column "Periodo di dodici mesi chiuso al 31 dicembre" exists
        if "Periodo di dodici mesi chiuso al 31 dicembre" in df.columns:
            # Get the name of the new column (second column)
            new_column_name = df.columns[1]

            # Rename the column using the value in the first row, second column
            df = df.rename(columns={new_column_name: df.iloc[0, 1]})

        # Remove the first row (header) since it's used for column renaming
        df = df.iloc[1:]

        # Check if the column "2022 2021" exists
        if '2022 2021' in df.columns:
            # Split the "2022 2021" column into two columns and drop the original
            df[['2022', '2021']] = df['2022 2021'].str.split(expand=True)
            df = df.drop(columns=['2022 2021'])

        # Fill NaN values with 0
        df = df.fillna(0)
        if not any(df["Name"].str.contains("ATTIVITA")) and any(df["Name"].str.contains("Immobili, Impianti e macchinari")):
            # If not present, insert a new row with values for ATTIVITA
            new_row_attivita = pd.Series(["ATTIVITA", 0, 0], index=df.columns)
            # Use loc to insert the new row at position 1
            df = pd.concat([df.iloc[:0], pd.DataFrame([new_row_attivita]), df.iloc[1:]], ignore_index=True)
            # Reset the index to start from 1
            df.index = range(1, len(df) + 1)
        if not any(df["Name"].str.contains("Ricavi")) and any(df["Name"].str.contains("Costi del contratto")):
            # If not present, insert a new row with values for Ricavi
            new_row_attivita = pd.Series(["Ricavi", 0, 0], index=df.columns)
            # Use loc to insert the new row at position 1
            df = pd.concat([df.iloc[:0], pd.DataFrame([new_row_attivita]), df.iloc[1:]], ignore_index=True)
            # Reset the index to start from 1
            df.index = range(1, len(df) + 1)    
        df = df.drop_duplicates(subset=['Name'])
        df = df[df['Name'] != 0]    
        # print(df)    
        if df.at[1, "Name"] == 'Ricavi' or df.at[1, "Name"] == 'RICAVI':
            valid_indices = [0, 9, 7, 15, 21]
        else:
            valid_indices = [0, 13, 34, 12, 17, 26,9,29,21]

        for index in valid_indices:
            # Check if the index is within the valid range
            if 0 <= index < len(df):
                row_at_index = df.iloc[index]
                rows.append(row_at_index)
            else:
                print(f"Index {index} is out of bounds.")
    return rows     
