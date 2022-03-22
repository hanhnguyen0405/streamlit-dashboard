import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect
import pandas as pd
import datetime

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        'https://www.googleapis.com/auth/drive'
    ],
)
conn = connect(credentials=credentials)


# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
def get_data(sheet_url):
    query = f'SELECT * FROM "{sheet_url}"'
    rows = conn.execute(query, headers=1)
    df = pd.DataFrame(rows)
    return df


filtered_sheet = st.secrets["private_gsheets_url_filtered"]
unfiltered_sheet = st.secrets["private_gsheets_url_unfiltered"]

# ---- The actual table rendering part ----

st.markdown('# Screener')

is_rendered = False

if not is_rendered or st.button('Refresh'):
    st.empty()
    st.markdown(f'#### Last refreshed: {datetime.datetime.now()}')
    st.dataframe(get_data(filtered_sheet), 400, 200)
    