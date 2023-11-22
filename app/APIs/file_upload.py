from flask import jsonify, make_response, request, Blueprint, current_app
from app import app, db
from app.models import Company, ProfitAndLoss, BalanceSheet
from werkzeug.utils import secure_filename
import os
from app.scripts.file1 import extract_data_from_pdf_one
from app.scripts.file2 import extract_data_from_pdf_two
from app.scripts.file3PdfImages import extract_data_from_pdf_three
from app.scripts.file4 import extract_data_from_pdf_foure
from app.scripts.file5 import extract_data_from_pdf_five
import tabula
import pandas as pd
from datetime import datetime
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

file_upload_bp = Blueprint('file-upload', __name__)

# -----------------------Upload Pdf files and save the results in the database-------------------------


def read_table(pdf_file,value1,value2,condition):
    tables = tabula.read_pdf(pdf_file, pages="all")
    # Initialize counts for '2021' and '2020'
    count_1 = 0
    count_2 = 0
    for table in tables:
        df = pd.DataFrame(table)
        # Update counts based on the presence of '2021' and '2020'
        count_1 += df.columns.tolist().count(value1)
        count_2 += df.columns.tolist().count(value2)
    # Check if '2021' and '2020' are present multiple times across all tables
    # print(count_1,count_2)
    has_multiple_1 = count_1 >= condition
    has_multiple_2 = count_2 >= condition
    if has_multiple_1 and has_multiple_2:
        return True
    return False

# Configure the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Ensure the upload folder exists, create it if not
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}



def data_dump_database(data,company):
    profit_loss_words = [
    "Revenue", "Ricavi","Operating profit","Totale Costi","Accantonamenti","UTILE NETTO",
    "Impairment losses of financial assets","Tax expense","netto degli effetti fiscali","Altre componenti del conto economico complessivo",
    "Operating Income", "Utile Operativo","Owners of the parent","Quota parte di utili di società collegate","Utile operativo",    "Operating Profit", "Risultato Operativo","Costiperserviziegodimentibeniditerzi",
    "EBIT (Earnings Before Interest and Taxes)", "EBIT",
    "Depreciation", "Ammortamenti","Terzi","Costi per benefici dei dipendenti",
    "Amortization", "Accantonamenti","Utileperditaanteimposte",
    "Altricostioperativi","PROVENTIEONERIFINANZIARI",
    "Depreciation & Amortization", "Depreciation & Amortization",
    "Profit Before Taxes", "Utile Ante Imposte",
    "Net Profit", "Utile (perdita) ante-imposte",
    "Net Income", "Utile Netto","Impairment losses of financial assets and contract assets",
    "Net Income", "Utile (perdita) Netto"]
    for rows in data:  
        possible_keys_2021=['2021','31/12/2021',]
        possible_keys_2022=['2022','31/12/2022']
        possible_keys_2004=['2004','31 dicembre 2004']
        possible_keys_2005=['2005','31 dicembre 2005']
        # Create a new company
        if any(rows['Name'].casefold() == term.split(',')[0].strip().casefold() for term in profit_loss_words):
                insert_data_profit_loss = ProfitAndLoss(
                company_id=company,
                field_name=rows.get('Name', 0),  # If 'Name' is missing, default to an empty string
                year_2020=rows.get('2020', 0),   # If '2020' is missing, default to an empty string
                year_2021=rows.get('2021', 0),   # If '2021' is missing, default to an empty string
                year_2022=rows.get('2022', 0),   # If '2022' is missing, default to an empty string
                year_2023=rows.get('2023', 0),    # If '2023' is missing, default to an empty string
                year_2003=rows.get('2003', 0),    # If '2023' is missing, default to an empty string
                year_2004 = next((rows.get(key, '0') for key in possible_keys_2004 if key in rows), '0'),
                year_2005 = next((rows.get(key, '0') for key in possible_keys_2005 if key in rows), '0'),
                )
                # Add the new company to the database
                db.session.add(insert_data_profit_loss)
                db.session.commit()        
        else:        
            insert_data_balance_sheet = BalanceSheet(
            company_id=company,
            field_name=rows.get('Name', 0),  # If 'Name' is missing, default to an empty string
            year_2020=rows.get('2020', 0),   # If '2020' is missing, default to an empty string
            year_2021 = next((rows.get(key, '0') for key in possible_keys_2021 if key in rows), '0'),
            year_2022 = next((rows.get(key, '0') for key in possible_keys_2022 if key in rows), '0'),
            year_2023=rows.get('2023', 0),    # If '2023' is missing, default to an empty string
            year_2003=rows.get('2003', 0),    # If '2023' is missing, default to an empty string
            year_2004 = next((rows.get(key, '0') for key in possible_keys_2004 if key in rows), '0'),
            year_2005 = next((rows.get(key, '0') for key in possible_keys_2005 if key in rows), '0'),
            )
            # Add the new company to the database
            db.session.add(insert_data_balance_sheet)
            db.session.commit()
    return True


# Check if a filename has a valid extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@file_upload_bp.route('/file-upload/<int:id>', methods=['GET'])
def upload_file(id):
    try:
        current_app.logger.info(f"{timestamp} - Received a {request.method} request to {request.url}")
        # Check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "No file part"})
        file = request.files['file']
        # Check if a file is selected
        if file.filename == '':
            return jsonify({"status": "error", "message": "No selected file"})
        # Check if the file has an allowed extension
        if file and allowed_file(file.filename):
            company = Company.query.get(id)
            if not company:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Company record not found",
                }), 404)
            company= company.as_dict()
            # Secure the filename to prevent directory traversal
            filename = secure_filename(file.filename)
            # Save the file to the upload folder
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # data = read_table(file_path,"2020","2021",10)
            if read_table(file_path,"2020","2021",10):
                data = extract_data_from_pdf_one(file_path)
                data_dump_database(data,company.get('id'))
            elif read_table(file_path,"2022","2021",10):
                data = extract_data_from_pdf_one(file_path)
                data_dump_database(data,company.get('id')) 
            elif read_table(file_path,"2003","2004",1):
                data = extract_data_from_pdf_foure(file_path)
                data_dump_database(data,company.get('id')) 
            elif read_table(file_path,"31/12/2022","31/12/2021",3):
                data = extract_data_from_pdf_five(file_path)
                data_dump_database(data,company.get('id')) 
            else:
                data = extract_data_from_pdf_three(file_path)
                data_dump_database(data,company.get('id'))  
            return jsonify({
                "status": "success",
                "message": "File uploaded and data inserted successfully",
                "company_name": company.get('company_name'),
                "filename": filename
            })
        return jsonify({"status": "error", "message": "Invalid file type"})
    except Exception as e:
        current_app.logger.error(f'{timestamp} - An error occurred on URL {request.url}: {str(e)}')
        return jsonify({"status": "error", "message": str(e)}), 500

