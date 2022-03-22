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


# ---- Page rendering ----
_zipcode_list = []
df = None


def refresh_page():
    st.empty()
    st.markdown(f'#### Last refreshed: {datetime.datetime.now()}')

    global _zipcode_list, df
    df = get_data(filtered_sheet)
    _zipcode_list = list(set(df.zipcode))

    st.dataframe(df, 2000, 800)


def update_page(selected_zipcodes):
    global df
    if selected_zipcodes:
        updated_df = df[~df.zipcode.apply(lambda x: x in selected_zipcodes)]
        st.dataframe(updated_df, 2000, 800)
    else:
        st.dataframe(df, 2000, 800)

        
# ---- The actual table rendering part ----

st.markdown('# Screener')

is_rendered = False
refresh_clicked = st.button('Refresh')

selected_zipcodes = st.multiselect('Select zipcode(s)', _zipcode_list)
zipcode_clicked = st.button('Apply zipcode selection')

if not is_rendered or refresh_clicked:
    refresh_page()
    is_rendered = True

if zipcode_clicked:
    refresh_page()
    
