from flask import Blueprint, jsonify, current_app
from flask import jsonify, make_response, request
from app.models import ProfitAndLoss
from app import db
from app.helper.msg import RECORD_NOT_FOUND, RECORD_UPDATED, RECORD_DELETED, RECORD_FOUND
from sqlalchemy import desc
import json
from datetime import datetime
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


profit_and_loss_bp = Blueprint('profit-and-loss', __name__)



"""
    Get all profit-and-loss records with associated ProfitAndLoss and BalanceSheet data.

    Request:
    - Method: GET
    - Endpoint: /profit-and-loss

    Response:
    - 200 OK: Records retrieved successfully
    - 404 Not Found: No Records found
    - 500 Internal Server Error: An unexpected error occurred
"""
@profit_and_loss_bp.route('/profit-and-loss', methods=['GET'])
def get_all_profit_and_loss():
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
            finances = ProfitAndLoss.query.order_by(getattr(ProfitAndLoss, order_by)).paginate(
                page=page, per_page=per_page, error_out=True, max_per_page=20
            )
        else:
            finances = ProfitAndLoss.query.order_by(desc(getattr(ProfitAndLoss, order_by))).paginate(
                page=page, per_page=per_page, error_out=True, max_per_page=20
            )
        if not finances:
            return make_response(jsonify(RECORD_NOT_FOUND), 404)
        finances_data = [finance.as_dict() for finance in finances]
        response = {
            **RECORD_FOUND,
            "data": finances_data,
            "pagination": {
                "total_pages": finances.pages,
                "current_page": finances.page,
                "total_records": finances.total,
                "per_page": per_page,
            }
        }
        return jsonify(response)
    except Exception as e:
            current_app.logger.error(f'{timestamp} - An error occurred on URL {request.url}: {str(e)}')
            return jsonify({"status": "error", "message": str(e)}), 500
    

"""
    Get a specific profit-and-loss record with associated ProfitAndLoss and BalanceSheet data.

    Request:
    - Method: GET
    - Endpoint: /profit-and-loss/<id>
    - Path Variable: id (profit-and-loss ID)

    Response:
    - 200 OK: Finance records retrieved successfully
    - 404 Not Found: Record not found
    - 500 Internal Server Error: An unexpected error occurred
"""
@profit_and_loss_bp.route('/profit-and-loss/<int:id>')
def get_profit_and_loss(id):
    try:
        current_app.logger.info(f"{timestamp} - Received a {request.method} request to {request.url}")
        finances = ProfitAndLoss.query.get(id)
        if not finances:
            return make_response(jsonify(RECORD_NOT_FOUND), 404)
        finance_data = finances.as_dict()
        response = {
            **RECORD_FOUND,
            "data": finance_data,
        }
        return jsonify(response)
    except Exception as e:
            current_app.logger.error(f'{timestamp} - An error occurred on URL {request.url}: {str(e)}')
            return jsonify({"status": "error", "message": str(e)}), 500


"""
    Delete a specific profit-and-loss record.

    Request:
    - Method: DELETE
    - Endpoint: /profit-and-loss/<id>
    - Path Variable: id (profit-and-loss ID)

    Response:
    - 200 OK: Record deleted successfully
    - 404 Not Found: Record not found
    - 500 Internal Server Error: An unexpected error occurred
"""
@profit_and_loss_bp.route('/profit-and-loss/<int:id>', methods=['DELETE'])
def delete_profit_and_loss(id):
    try:
        current_app.logger.info(f"{timestamp} - Received a {request.method} request to {request.url}")
        finance = ProfitAndLoss.query.get(id)
        if not finance:
            return make_response(jsonify(RECORD_NOT_FOUND), 404)
        db.session.delete(finance)
        db.session.commit()
        return jsonify(RECORD_DELETED)
    except Exception as e:
            current_app.logger.error(f'{timestamp} - An error occurred on URL {request.url}: {str(e)}')
            return jsonify({"status": "error", "message": str(e)}), 500


"""
    Update a specific profit-and-loss record.

    Request:
    - Method: PUT
    - Endpoint: /profit-and-loss/<id>
    - Path Variable: id (profit-and-loss ID)
    - Body: JSON with updated data

    Response:
    - 200 OK: Record updated successfully
    - 404 Not Found: Record not found
    - 500 Internal Server Error: An unexpected error occurred
"""
@profit_and_loss_bp.route('/profit-and-loss/<int:id>', methods=['PUT'])
def update_profit_and_loss(id):
    try:
        current_app.logger.info(f"{timestamp} - Received a {request.method} request to {request.url}")
        finance = ProfitAndLoss.query.get(id)
        if not finance:
            return make_response(jsonify(RECORD_NOT_FOUND), 404)
        data = request.get_json()
        # Update fields
        finance.update(data)  # Assuming you have an update method in your Finance model
        db.session.commit()
        return jsonify(RECORD_UPDATED)
    except Exception as e:
            current_app.logger.error(f'{timestamp} - An error occurred on URL {request.url}: {str(e)}')
            return jsonify({"status": "error", "message": str(e)}), 500    