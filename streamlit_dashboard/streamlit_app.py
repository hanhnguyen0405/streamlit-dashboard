import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect
import pandas as pd
from streamlit_autorefresh import st_autorefresh

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

# update every 5 mins
st_autorefresh(interval=5 * 60 * 1000, key="dataframerefresh")

st.dataframe(get_data(filtered_sheet))
