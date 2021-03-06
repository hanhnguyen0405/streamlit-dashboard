import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect
import pandas as pd
import datetime
import uuid


# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        'https://www.googleapis.com/auth/drive'
    ],
)
conn = connect(credentials=credentials)


def infer_type(x):
    try:
        return x.astype(float) if '.' in x.iloc[0] else x.astype(int)
    except ValueError:
        return x.astype(str)


filtered_sheet = st.secrets["private_gsheets_url_filtered"]
unfiltered_sheet = st.secrets["private_gsheets_url_unfiltered"]


# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
def get_data(sheet_url):
    query = f'SELECT * FROM "{sheet_url}"'
    rows = conn.execute(query, headers=1)
    df = pd.DataFrame(rows)

    df = df.apply(infer_type)
    df.rename(columns=lambda c: c.replace('_', ' ').title(), inplace=True)

    return df


# ---- Page rendering ----
st.session_state['zipcode_list'] = []
df = None
st.session_state['selected_zipcodes'] = []


def refresh_page():
    global df
    print('Query new data from Google Sheet')
    df = get_data(filtered_sheet)

    st.session_state['df_container'] = st.empty()
    with st.session_state['df_container'].container():
        st.markdown(f'#### Last refreshed: {datetime.datetime.now()}')
        st.dataframe(df, 2000, 800)

        
# ---- The actual table rendering part ----

st.markdown('# Screener')

st.session_state['is_rendered'] = False
refresh_clicked = st.button('Refresh')

if not st.session_state['is_rendered'] or refresh_clicked:
    refresh_page()
    st.session_state['is_rendered'] = True
    