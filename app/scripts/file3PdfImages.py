from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import re
import pandas as pd
from datetime import datetime
import os


def extract_data_from_pdf_three(pdf_path):
    rows=[]
    def table_header(extracted_text):
        result=[]
        start_printing = False
        lines = extracted_text.split('\n')
        for item in lines:
            if not item.strip():
                    continue
            # Check if the line contains only one word
            if (len(item.split()) == 1 or len(item.split()) == 2) and any(c.isalpha() for c in item):
                start_printing = True
            # Print the line if the flag is set
            if start_printing:
                if len(item.split()) ==1 or len(item.split()) ==2 and not re.match(r'^\d+(\.\d+)?$', item):
                    # print(item)
                    result.append(item)
                    break
        # print(result)
        return result           
        # return result          
    tables = []


    # Provide the path to the Tesseract executable (Windows only)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Function to perform OCR on an image
    def ocr_image(image_path):
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text

    images = convert_from_path(pdf_path)

    result = []
    for i, image in enumerate(images):
            timestamp = datetime.now().strftime("%Y-%m-%d-%H_%M_%S")  # Use underscores instead of colons
            image_path = os.path.join('images', f'page_{i + 1}_{timestamp}.png')  # Save each page in the folder
            # image_path = f'page_{i + 1}_{timestamp}.png'  # Save each page as an image
            image.save(image_path, 'PNG')

            extracted_text = ocr_image(image_path)
            # print("here are text",extracted_text)
            # Split the text into lines
            lines = extracted_text.split('\n')
            # print(lines)
            head = table_header(extracted_text)
            if head[0]=='Ricavi' or head[0]=='RICAVI' or head[0]=='Attivo' or head[0]=='ATTIVITA':
                data_list=list(filter(None,lines))
                # print(data_list)
                # Flag to indicate when to start printing
                start_printing = False
                # Iterate through the list
                df = pd.DataFrame(columns=["Name","2023","2022"])
                for item in data_list:
                    if item=='Ricavi' or item=='RICAVI' or item=='Attivo' or item=='ATTIVITA':
                        # Set the flag to start printing from the next item
                        start_printing = True
                    elif start_printing:
                        # Print the item if the flag is set
                        # print(item)
                        result_string = re.sub(r'[()]', '', item)
                        input_string = result_string

                        # Initialize variables
                        text_part = ""
                        numeric_part = ""
                        numeric_parts = []

                        # Iterate through the characters in the input string
                        for char in input_string:
                            if char.isalpha() or char in [',']:
                                # If the character is a letter or comma, add it to the text part
                                text_part += char
                                if numeric_part:
                                    # If numeric part was being built, add it to the list
                                    numeric_parts.append(numeric_part)
                                    numeric_part = ""
                            elif char.isdigit() or char == '.' or char == '-':
                                # If the character is a digit, dot (for decimal points), or minus sign (for negative numbers), add it to the numeric part
                                numeric_part += char
                            elif char.isspace():
                                # If the character is a space, add the numeric part to the list
                                if numeric_part:
                                    numeric_parts.append(numeric_part)
                                    numeric_part = ""

                        # Add the last numeric part if any
                        if numeric_part:
                            numeric_parts.append(numeric_part)

                        # Check if the last element in numeric_parts is followed by a non-numeric character (excluding spaces)
                        if numeric_parts and not all(char.isspace() or char.isdigit() for char in input_string.split(numeric_parts[-1])[-1]):
                            # If yes, consider the last element as part of the text
                            text_part += numeric_parts.pop()

                        # Remove trailing spaces and split the numeric parts at spaces
                        text_part = text_part.strip()
                        numeric_parts = [part.strip() for part in ' '.join(numeric_parts).split()]
                        # print(item[0])
                        final_results_table=[]
                        final_results_table=[]
                        if len(text_part)!=0:
                            if len(numeric_parts)==0:
                                numeric_parts.append(0)
                                numeric_parts.append(0)
                                numeric_parts.append(0)
                            elif len(numeric_parts) ==2:
                                numeric_parts.insert(0,0)
                            elif len(numeric_parts)==1:
                                numeric_parts.append(0)
                                numeric_parts.append(0)
                            final_results_table.insert(0,text_part)
                            final_results_table.insert(1,numeric_parts[1])
                            final_results_table.insert(1,numeric_parts[2])
                        if final_results_table == []:
                            continue
                        df = df._append({"Name": final_results_table[0], "2023": final_results_table[1], "2022": final_results_table[2]}, ignore_index=True)      
                ricavi_present = any(result[0] == head[0] for result in df)
                if not ricavi_present:
                            new_row = {"Name": head[0], "2023": 0, "2022": 0}
                            df = pd.concat([pd.DataFrame([new_row]), df], ignore_index=True)
                if head[0] == 'Ricavi' or head[0] == 'RICAVI':
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











