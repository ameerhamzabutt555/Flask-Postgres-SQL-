import os

db_user = os.getenv("DB_USER", "postgres")
db_ip = os.getenv("DB_IP", "127.0.0.1")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "finance_data")
db_password = os.getenv("DB_PASSWORD", "12345678")
scret_key = os.getenv("SECRET_KEY", "ddddjjjjj")
class Config:
    SECRET_KEY = scret_key
    SQLALCHEMY_DATABASE_URI = f'postgresql://{db_user}:{db_password}@{db_ip}:{db_port}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
