from flask import Blueprint, jsonify, current_app
from flask import jsonify, make_response, request
from app.models import Company
from app import db
from app.helper.msg import RECORD_NOT_FOUND, RECORD_UPDATED, RECORD_DELETED, RECORD_FOUND,COMPANY_NAME_REQUIRED,COMPANY_ALREADY_EXIST,COMPANY_CREATED
from sqlalchemy import desc
import json
from datetime import datetime
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

company_bp = Blueprint('company', __name__)

"""
Create a new company record.

Request:
- Method: POST
- Endpoint: /create_company
- Body: JSON with company_name

Response:
- 201 Created: Company created successfully
- 400 Bad Request: Invalid request data
- 403 Company with the given name already exists
- 404 Not Found: 
- 500 Internal Server Error: An unexpected error occurred
"""
@company_bp.route('/create_company', methods=['POST'])
def create_company():
    try:
        current_app.logger.info(f"{timestamp} - Received a {request.method} request to {request.url}")
        # Get data from the request
        data = request.get_json()
        # Validate if 'company_name' is present in the data
        if 'company_name' not in data or not data['company_name']:
            return jsonify(COMPANY_NAME_REQUIRED), 400
        # Check if the company with the given name already exists
        existing_company = Company.query.filter_by(company_name=data['company_name']).first()
        if existing_company:
            return jsonify(COMPANY_ALREADY_EXIST), 403
        # Create a new company
        new_company = Company(company_name=data['company_name'])
        # Add the new company to the database
        db.session.add(new_company)
        db.session.commit()
        return jsonify({
            **COMPANY_CREATED,
            "data": new_company.as_dict()
        }), 201
    except Exception as e:
        current_app.logger.error(f'{timestamp} - An error occurred on URL {request.url}: {str(e)}')
        return jsonify({"status": "error", "message": str(e)}), 500



"""
    Get all company records with associated ProfitAndLoss and BalanceSheet data.

    Request:
    - Method: GET
    - Endpoint: /company

    Response:
    - 200 OK: Records retrieved successfully
    - 404 Not Found: No Records found
    - 500 Internal Server Error: An unexpected error occurred
"""
# Read All Transactions
@company_bp.route('/company', methods=['GET'])
def get_all_companies():
    try:
        current_app.logger.info(f"{timestamp} - Received a {request.method} request to {request.url}")
        data = request.get_data(as_text=True)
        if data is "":
            # Set default values if JSON data is not present
            page = 1
            per_page = 10
            order_by = 'id'
            order = 'asc'
        else:
            data = json.loads(data)
            page = data.get('page', 1)
            per_page = data.get('per_page', 10)
            order_by = data.get('order_by', 'id')
            order = data.get('order', 'asc')
        # Perform the query using pagination with ordering
        if order == 'asc':
            companies = Company.query.order_by(getattr(Company, order_by)).paginate(
                page=page, per_page=per_page, error_out=True, max_per_page=20
            )
        else:
            companies = Company.query.order_by(desc(getattr(Company, order_by))).paginate(
                page=page, per_page=per_page, error_out=True, max_per_page=20
            )
        if not companies:
            return make_response(jsonify(RECORD_NOT_FOUND), 404)
        # Create a list to store company data with associated ProfitAndLoss and BalanceSheet
        companies_data = []
        
        for company in companies:
            # Convert the Company instance to a dictionary
            company_data = company.as_dict()
            # Add associated ProfitAndLoss data to the dictionary
            company_data['profit_and_loss'] = [pnl.as_dict() for pnl in company.profit_and_loss]
            # Add associated BalanceSheet data to the dictionary
            company_data['balance_sheet'] = [bs.as_dict() for bs in company.balance_sheet]
            # Append the dictionary to the list
            companies_data.append(company_data)
        response = {
            **RECORD_FOUND,
            "data": companies_data,
            "pagination": {
                "total_pages": companies.pages,
                "current_page": companies.page,
                "total_records": companies.total,
                "per_page": per_page,
            }
        }

        return jsonify(response)

    except Exception as e:
        current_app.logger.error(f'{timestamp} - An error occurred on URL {request.url}: {str(e)}')
        return jsonify({"status": "error", "message": str(e)}), 500


"""
    Get a specific company record with associated ProfitAndLoss and BalanceSheet data.

    Request:
    - Method: GET
    - Endpoint: /company/<id>
    - Path Variable: id (company ID)

    Response:
    - 200 OK: Finance records retrieved successfully
    - 404 Not Found: Record not found
    - 500 Internal Server Error: An unexpected error occurred
"""
@company_bp.route('/company/<int:id>')
def get_finance(id):
    try:
        current_app.logger.info(f"{timestamp} - Received a {request.method} request to {request.url}")
        company = Company.query.get(id)
        if not company:
            return make_response(jsonify(RECORD_NOT_FOUND), 404)

        # Convert the Company instance to a dictionary
        finance_data = company.as_dict()

        # Add associated ProfitAndLoss data to the dictionary
        finance_data['profit_and_loss'] = [pnl.as_dict() for pnl in company.profit_and_loss]

        # Add associated BalanceSheet data to the dictionary
        finance_data['balance_sheet'] = [bs.as_dict() for bs in company.balance_sheet]

        response = {
            **RECORD_FOUND,
            "data": finance_data,
        }

        return jsonify(response)
    
    except Exception as e:
        current_app.logger.error(f'{timestamp} - An error occurred on URL {request.url}: {str(e)}')
        return jsonify({"status": "error", "message": str(e)}), 500


"""
    Delete a specific company record.

    Request:
    - Method: DELETE
    - Endpoint: /company/<id>
    - Path Variable: id (company ID)

    Response:
    - 200 OK: Record deleted successfully
    - 404 Not Found: Record not found
    - 500 Internal Server Error: An unexpected error occurred
"""
@company_bp.route('/company/<int:id>', methods=['DELETE'])
def delete_finance(id):
    try:
        current_app.logger.info(f"{timestamp} - Received a {request.method} request to {request.url}")
        company = Company.query.get(id)
        if not company:
            return make_response(jsonify(RECORD_NOT_FOUND), 404)
        db.session.delete(company)
        db.session.commit()
        return jsonify(RECORD_DELETED)
    except Exception as e:
        current_app.logger.error(f'{timestamp} - An error occurred on URL {request.url}: {str(e)}')
        return jsonify({"status": "error", "message": str(e)}), 500


"""
    Update a specific company record.

    Request:
    - Method: PUT
    - Endpoint: /company/<id>
    - Path Variable: id (company ID)
    - Body: JSON with updated data

    Response:
    - 200 OK: Record updated successfully
    - 404 Not Found: Record not found
    - 500 Internal Server Error: An unexpected error occurred
"""
@company_bp.route('/company/<int:id>', methods=['PUT'])
def update_finance(id):
    try:
        current_app.logger.info(f"{timestamp} - Received a {request.method} request to {request.url}")
        company = Company.query.get(id)
        if not company:
            return make_response(jsonify(RECORD_NOT_FOUND), 404)
        data = request.get_json()
        # Update fields
        company.update(data)  # Assuming you have an update method in your company model
        db.session.commit()
        return jsonify(RECORD_UPDATED)
    except Exception as e:
        current_app.logger.error(f'{timestamp} - An error occurred on URL {request.url}: {str(e)}')
        return jsonify({"status": "error", "message": str(e)}), 500