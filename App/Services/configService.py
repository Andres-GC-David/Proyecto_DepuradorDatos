import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class ConfigService:
    @staticmethod
    def get_oracle_credentials():
        user = os.getenv('ORACLE_USER')
        password = os.getenv('ORACLE_PASSWORD')
        dsn = os.getenv('ORACLE_DSN')
        if not user or not password or not dsn:
            raise ValueError("Missing Oracle credentials in .env file")
        return user, password, dsn
