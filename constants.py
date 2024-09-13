from dotenv import load_dotenv
import os

load_dotenv()

# Database constant class
class DatabaseConstants:
    host: str = os.getenv("HOST")
    user: str = os.getenv("USER")
    database: str = os.getenv("DATABASE")
    password: str = os.getenv("PASSWORD")

def get_dbconstants() -> DatabaseConstants:
    return DatabaseConstants()

# Google-Sheet constant class
class GoogleSheetConstants:
    scopes: list[str] = os.getenv('SCOPES').split(",")
    google_cred_filepath: str = os.getenv("GOOGLE_CREDENTIAL_FILEPATH")
    google_sheet_id: str = os.getenv("GOOGLE_SHEET_ID")

def get_googlesheet_constants() -> GoogleSheetConstants:
    return GoogleSheetConstants()