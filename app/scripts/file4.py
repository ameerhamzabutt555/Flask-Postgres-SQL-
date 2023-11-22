import tabula
import pandas as pd


def extract_data_from_pdf_foure(pdf_path):
    final_rows=[]
    def push_to_final_rows(df):
        if df.at[0, 'Name'] == 'Ricavi' or df.at[0, 'Name'] == 'RICAVI':
            valid_indices = [0, 9, 7, 15, 21]
        else:
            valid_indices = [0, 13, 34, 12, 17, 26,9,29,21]

        for index in valid_indices:
            # Check if the index is within the valid range
            if 0 <= index < len(df):
                row_at_index = df.iloc[index]
                final_rows.append(row_at_index)
            else:
                print(f"Index {index} is out of bounds.")
        return 


    tables = tabula.read_pdf(pdf_path, pages='all')
    for i, table in enumerate(tables):
        # print(tables)
        # Check if the table contains "ASSETS" and "Ricavi"
        if any(table.applymap(lambda cell: "ASSETS" in str(cell) or "Ricavi" in str(cell) or "Ricavi" in str(cell)).values.flatten()):
            # print(f"Table {i + 1}:")
            df = pd.DataFrame(table)
            if len(df.columns) > 4:
                # Task 1: Rename the 'In millions of CHF' column to 'Name'
                df.rename(columns={'In millions of CHF': 'Name'}, inplace=True)

                # Task 2: Remove columns 1 and 2
                df.drop(columns=['Notes', 'Unnamed: 0'], inplace=True)

                # Task 3: Combine '2004' and 'Unnamed: 1' columns
                df['2004'] = df['2004'].fillna(df['Unnamed: 1'])
                df.drop(columns=['Unnamed: 1'], inplace=True)

                # Task 4: Combine '2003' and 'Unnamed: 2' columns
                df['2003'] = df['2003'].fillna(df['Unnamed: 2'])
                df.drop(columns=['Unnamed: 2'], inplace=True)
                df.fillna(0, inplace=True)
                df.drop_duplicates(inplace=True)
                push_to_final_rows(df)
            else:
                df = pd.DataFrame(table)
                df.rename(columns={'Schema di conto economico (appendice allo Ias 1)': 'Name','Unnamed: 0':2005,'Unnamed: 1':2004}, inplace=True)
                # Find the index where "Name" is equal to "Ricavi"
                ricavi_index = df[df['Name'] == 'Ricavi'].index[0]
                # Slice the DataFrame from the "Ricavi" index onward
                df = df.iloc[ricavi_index:].reset_index(drop=True)
                df.drop_duplicates(inplace=True)
                df['Name'] = df['Name'].ffill()
                # Fill remaining NaN values with 0
                df = df.fillna(0)
                # Reset the index
                df = df.reset_index(drop=True)
                push_to_final_rows(df)

                
    return final_rows