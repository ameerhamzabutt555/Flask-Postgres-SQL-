import tabula
import pandas as pd






def extract_data_from_pdf_two(pdf_path):
    tables_list = []
    rows = []


    # Function to clean and convert numeric values
    def clean_and_convert(value):
        if isinstance(value, str):
            # Remove thousands separators (periods) and convert to float
            cleaned_value = value.replace('.', '').replace(',', '.')
            return pd.to_numeric(cleaned_value, errors='coerce')
        return value

    # Read the table from the PDF and get the page numbers
    tables = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)
    for page_number, table in enumerate(tables, start=1):
        df = pd.DataFrame(table)
        if not df.empty and ('2022' in df.columns or '2021' in df.columns or '31 Dec' in df.columns or '31 Dec 2021' in df.columns or '31 Dec 2022' in df.columns or '31 December' in df.columns  or '31 December 2021' in df.columns or '31 December 2022' in df.columns):
        # if df.empty or not any(df.columns.str.match(r'20[12]\d')):

            # print("Page:", page_number)  # Print the page number

            # Rename the first column to "Name"
            df = df.rename(columns={df.columns[0]: "Name"})
            # Fill NaN values in "Name" column with an empty string
            df['Name'] = df['Name'].fillna('')
            # Clean the "Name" column
            df['Name'] = df['Name'].str.replace(r'\s*\([^)]*\)\s*', '', regex=True)
            df['Name'] = df['Name'].str.replace(r'IAS\s+\d+\.\d+', '', regex=True)
            df['Name'] = df['Name'].str.replace(r'IFRS (\d+\.\d+)\([^)]*\)', r'IFRS \1', regex=True)

            # Check if the "Name" column contains a single character
            if df['Name'].str.match(r'^(A|B|IFRS 7\.24C|IFRS 5\.33|\s)*$', case=False).all():

                # If all values in "Name" are single characters, drop the entire column
                df = df.drop(columns=['Name'])
                df= df.rename(columns={df.columns[0]: "Name"})
                df = df.dropna(subset=['Name'])
                df = df[df['Name'].str.strip() != '']
                if "2022" in df.columns and "2021" in df.columns:
                    selected_columns = ["Name", "2022", "2021"]
                elif "31 December" in df.columns and "31 December.1" in df.columns:
                    selected_columns = ["Name", "31 December", "31 December.1"]
                else:
                    continue
                df = df.fillna(0)
                df[selected_columns[1]] = df[selected_columns[1]].astype(str).str.replace(r'[\(\)]', '', regex=True)
                df[selected_columns[2]] = df[selected_columns[2]].astype(str).str.replace(r'[\(\)]', '', regex=True)    
                df[selected_columns[1]] = df[selected_columns[1]].apply(clean_and_convert)
                df[selected_columns[2]] = df[selected_columns[2]].apply(clean_and_convert)
                subset_df = df[selected_columns]
                tables_list.append(subset_df)
                # print(subset_df)
                # print(df)
            else:
                # Remove rows with NaN values in the "Name" column
                df = df.dropna(subset=['Name'])
                df = df[df['Name'].str.strip() != '']
                df = df.reset_index(drop=True)
                if "2022" in df.columns and "2021" in df.columns:
                    selected_columns = ["Name", "2022", "2021"]
                elif "31 Dec" in df.columns and "31 Dec.1" in df.columns:
                    selected_columns = ["Name", "31 Dec", "31 Dec.1"]
                elif "31 December 2021" in df.columns and "31 December 2022" in df.columns:
                    selected_columns = ["Name", "31 December 2021", "31 December 2022"]    
                elif "31 Dec 2021" in df.columns and "31 Dec 2022" in df.columns:
                    df = df.drop(columns=['Name'])
                    df = df.rename(columns={'Unnamed: 1': 'Name'}) 
                    selected_columns = ["Name", "31 Dec 2022", "31 Dec 2021"]
                elif "31 December" in df.columns and "31 December.1" in df.columns:
                    names = df["Name"].tolist()
                    if "IFRS.7.24A" in names:
                        df = df.drop(columns=['Name'])
                        df = df.rename(columns={'Unnamed: 1': 'Name'})  
                        selected_columns = ["Name", "31 December", "31 December.1"] 
                    selected_columns = ["Name", "31 December", "31 December.1"] 
                else:
                    continue
                df = df.fillna(0)
                df[selected_columns[1]] = df[selected_columns[1]].astype(str).str.replace(r'[\(\)]', '', regex=True)
                df[selected_columns[2]] = df[selected_columns[2]].astype(str).str.replace(r'[\(\)]', '', regex=True)
                df[selected_columns[1]] = df[selected_columns[1]].apply(clean_and_convert)
                df[selected_columns[2]] = df[selected_columns[2]].apply(clean_and_convert)
                subset_df = df[selected_columns]
                tables_list.append(subset_df)
                # print(subset_df)

        continue        

    for table in tables_list:
        # print(table)
            # List of exact keywords to check
        exact_keywords = [
                'Ricavi', 'Utile Operativo', 'Risultato Operativo', 'EBIT', 'Ammortamenti',
                'Accantonamenti', 'Utile Ante Imposte', 'Utile (perdita) ante-imposte',
                'Utile Netto', 'Utile (perdita) Netto', 'Attivo Fisso', 'Attività non correnti',
                'Crediti Commerciali', 'Debiti Commerciali', 'Rimanenze', 'Disponibilità liquide',
                'Passività Finanziarie', 'Debiti Banche', 'Finanziamenti', 'Patrimonio Netto',
                'Totale Patrimonio Netto', 'Totale Passività', 'Totale Attività'
            ]
        keywords = [
        'Revenues','Revenue', 'Operating Income', 'Operating Profit', 'EBIT',
        'Depreciation', 'Amortization', 'Depreciation & Amortization',
        'Profit Before Taxes', 'Net Profit', 'Net Income',
        'Non Current Assets', 'Fixed Assets', 'Trade Receivables',
        'Trade Payables', 'Inventories', 'Cash', 'Cash and Cash Equivalents',
        'Debt', 'Financial Debt',
        'Equity', 'Total Equity', 'Total Liabilities', 'Total Assets']
            
        # Convert keywords to lowercase (or uppercase) for case-insensitive matching
        exact_keywords = [keyword.lower() for keyword in exact_keywords]
        keywordss = [keyword.lower() for keyword in keywords]


        # Iterate through the final cleaned DataFrame
        for index, row in table.iterrows():
            name = str(row[table.columns[0]]).lower()  # Convert 'Name' to lowercase
            # Check if the 'Name' value exactly matches one of the keywords (case-insensitive)
            if name in exact_keywords or name in keywordss:
                # Print the row
                # print(row)
                rows.append(row)
    print(rows)            
    return rows


# table1 = 3  # Change this to the index of the row you want to add from table1
# table2 = 2

# # column_name = '2023'  # Change this to the column you want to add
# table1=tables_list[table1]
# table2=tables_list[table2]

# column_name1 = '2022'  # Change this to the column you want to add
# column_name2 = '31 Dec 2022'  # Change this to the column you want to add


# # Specify the row names from the "Name" column
# row_name1 = 'Carrying amount 1 January'  # Change this to the first row you want to add from cleaned_df1
# row_name2 = 'Short-term leases'  # Change this to the row you want to add from cleaned_df2

# # Perform the addition
# result = float(table1.loc[table1['Name'] == row_name1, column_name1].values[0]) + float(table2.loc[table2['Name'] == row_name2, column_name2].values[0])

# # Print the result
# print(f"Result of ({row_name1} {column_name1} + {row_name2} {column_name2}):")
# print(result)