from app import db
from sqlalchemy.orm import relationship

# Company Table
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationship with ProfitAndLoss table
    profit_and_loss = db.relationship('ProfitAndLoss', backref='company', lazy=True)

    # Relationship with BalanceSheet table
    balance_sheet = db.relationship('BalanceSheet', backref='company', lazy=True)

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# Profit and Loss Table
class ProfitAndLoss(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    field_name = db.Column(db.String(255), nullable=False)
    year_2020 = db.Column(db.String(255), nullable=True)
    year_2021 = db.Column(db.String(255), nullable=True)
    year_2022 = db.Column(db.String(255), nullable=True)
    year_2023 = db.Column(db.String(255), nullable=True)
    year_2003 = db.Column(db.String(255), nullable=True)
    year_2004 = db.Column(db.String(255), nullable=True)
    year_2005 = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# Balance Sheet Table
class BalanceSheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    field_name = db.Column(db.String(255), nullable=False)
    year_2020 = db.Column(db.String(255), nullable=True)
    year_2021 = db.Column(db.String(255), nullable=True)
    year_2022 = db.Column(db.String(255), nullable=True)
    year_2023 = db.Column(db.String(255), nullable=True)
    year_2003 = db.Column(db.String(255), nullable=True)
    year_2004 = db.Column(db.String(255), nullable=True)
    year_2005 = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
   
