import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from constants import get_googlesheet_constants

def df_to_gsheet(df: pd.DataFrame, sheet_name:str) -> None:
    # Get the constants needed to set up connection to the google sheet
    gs_constants = get_googlesheet_constants()

    # Create credentials from the google credential file
    credentials = Credentials.from_service_account_file(gs_constants.google_cred_filepath, scopes=gs_constants.scopes)

    # Authorize the user
    gc = gspread.authorize(credentials)

    # Open the google spreadsheet to store the dataframe
    gs = gc.open_by_key(gs_constants.google_sheet_id)

    # Create a new worksheet
    worksheet = gs.add_worksheet(title=sheet_name, rows=len(df), cols=len(df.columns))
    
    # Store the incoming dataframe to the new worksheet
    set_with_dataframe(worksheet, dataframe=df)
    print("File saved successfully!!")