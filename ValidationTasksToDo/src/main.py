# Libraries commum imports
import os.path

# Extra libraries imports
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# Import constants variables
from core.constants import (
    # The ID and range of a sample spreadsheet.
    SAMPLE_RANGE_NAME,
    SAMPLE_SPREADSHEET_ID
)


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def tranforming_data(values: list[list[str]]):
    """
        #### Create a DataFrame from values
            - values: list[list[str]]
            - return: DataFrame containing the values of the specified columns
    """

    headers_list = values[0]

    count_lists = sum(1 for item in values if isinstance(item, list))

    if count_lists == 0:
        print('No data found.')
        return

    values_list = values[1:]

    data = [headers_list, []]

    for item in values_list:
        for index, row in enumerate(item):
            if row == '':
                item[index] = 'None'
        data[1].append(item)

    df = pd.DataFrame(data[1], columns=data[0])

    for _, row in df.iterrows():
        painel = row.get('painel')
        shopping = row.get('shopping')
        date = row.get('data')
        maturidade = row.get('maturidade')
        responsavel = row.get('responsavel')
        validada = row.get('validada')
        erp = row.get('erp')
        data_resolucao = row.get('data resolucao')
        bullet = row.get('bullet')

        # print(painel, shopping, date, maturidade, responsavel, validada, erp, data_resolucao, bullet)

    return df.to_csv


def main():
    """
        #### Shows basic usage of the Sheets API.
            - return: Values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('./token.json'):
        creds = Credentials.from_authorized_user_file('./token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('./credentials.json'):
                print('Ops! "credentials.json" file not found, please make sure it exists!')
                return
            flow = InstalledAppFlow.from_client_secrets_file(
                './credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('./token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()

        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()

        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

    except HttpError as err:
        print(err)

    return values


if __name__ == '__main__':
    values = main()
    df = tranforming_data(values)
    print(df)