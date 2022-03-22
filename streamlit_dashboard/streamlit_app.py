import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect
import pandas as pd
import datetime

pd.set_option('display.max_colwidth', -1)

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

def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    return f'<a target="_blank" href="{link}">link</a>'


filtered_sheet = st.secrets["private_gsheets_url_filtered"]
unfiltered_sheet = st.secrets["private_gsheets_url_unfiltered"]

# ---- The actual table rendering part ----

st.markdown('# Screener')

is_rendered = False
clicked = st.button('Refresh')

if not is_rendered or clicked:
    st.empty()
    st.markdown(f'#### Last refreshed: {datetime.datetime.now()}')

    df = get_data(filtered_sheet)
    df['url'] = df['url'].apply(make_clickable)
    
    df = df.to_html(escape=False)
    st.write(df.style.pipe(make_pretty), unsafe_allow_html=True)

    # st.dataframe(df, 2000, 800)
    is_rendered = True
    
