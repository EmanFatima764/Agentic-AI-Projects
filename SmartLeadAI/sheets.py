import gspread
from google.oauth2.service_account import Credentials


def save_to_google_sheet(
    sheet_name: str,
    data_dict: dict,
    credentials_file: str = "credentials.json"
) -> dict:
    """
    Save the scraped website data and AI analysis
    into a Google Sheet.
    """

    # These permissions allow our app to access and edit Google Sheets
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets"
    ]

    try:
        # Load the Google service account credentials from our JSON file
        creds = Credentials.from_service_account_file(
            credentials_file,
            scopes=scopes
        )

        # Use the credentials to connect our Python app to Google Sheets
        client = gspread.authorize(creds)

        # Open the requested Google Sheet and use its first worksheet
        sheet = client.open(sheet_name).sheet1

        # Collect the information we want to save as one new row
        row_data = [
            data_dict.get("url"),
            data_dict.get("title"),
            data_dict.get("meta_description"),
            data_dict.get("ai_analysis")
        ]

        # Add the new lead to the next available row
        sheet.append_row(row_data)

        # Let the rest of the application know that everything worked
        return {
            "success": True
        }

    except Exception as e:
        # Return the error so we can understand what went wrong
        # without stopping the whole application
        return {
            "success": False,
            "error": str(e)
        }