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
st.session_state['zipcode_list'] = []
df = None
st.session_state['selected_zipcodes'] = []


def refresh_page():
    global df
    print('Query new data from Google Sheet')
    df = get_data(filtered_sheet)
    st.session_state['zipcode_list'] = list(set(df.zipcode))

    st.session_state['df_container'] = st.empty()
    st.session_state['df_container'].markdown(f'#### Last refreshed: {datetime.datetime.now()}')
    st.session_state['selected_zipcodes'] = st.session_state['df_container'].multiselect('Select zipcode(s)',
            st.session_state['zipcode_list'])
    st.session_state['df_container'].dataframe(df, 2000, 800)


def update_page():
    global df
    if st.session_state['selected_zipcodes']:
        updated_df = df[df.zipcode.apply(lambda x: x in st.session_state['selected_zipcodes'])]
    else:
        updated_df = df

    st.session_state['df_container'].empty()
    st.session_state['df_container'].dataframe(updated_df, 2000, 800)

        
# ---- The actual table rendering part ----

st.markdown('# Screener')

st.session_state['is_rendered'] = False
refresh_clicked = st.button('Refresh')

zipcode_clicked = st.button('Apply zipcode selection')

if not st.session_state['is_rendered'] or refresh_clicked:
    refresh_page()
    st.session_state['is_rendered'] = True

if zipcode_clicked:
    update_page()
    
