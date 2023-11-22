from app import app
from app.APIs.company import company_bp
from app.APIs.profit_and_loss import profit_and_loss_bp
from app.APIs.balance_sheet import balance_sheet_bp
from app.APIs.file_upload import file_upload_bp
import logging



# Set the logging level and format
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Optionally, add a handler to output logs to a file
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)

# Register blueprints for each resource
app.register_blueprint(company_bp)
app.register_blueprint(profit_and_loss_bp)
app.register_blueprint(balance_sheet_bp)
app.register_blueprint(file_upload_bp)






