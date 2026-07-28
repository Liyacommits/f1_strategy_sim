import streamlit as st
import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("BASE_API_URL")

def fetch_data(endpoint, params=None):

    if params is None:
        params = {}

    url = f"{BASE_URL}{endpoint}"
    full_url = requests.Request(method="GET", url=url, params=params).prepare().url
    response = requests.get(full_url)
    response.raise_for_status()
    return pd.DataFrame(response.json())

@st.cache
def fetch_meetings(year, country):
    df = fetch_data("meetings", {"year": year, "country_name": country})
    if df.empty:
        st.error("No data found")
        return pd.DataFrame()

    df['label'] = df['meeting_name'] + " - " + df['location']
    df = df.sort_values(by=['meeting key'], ascending=False)
    return df[['meeting_key', 'label', 'year']].drop_duplicates()

@st.cache
def fetch_sessions(meeting_key):
    df = fetch_data("sessions", {"meeting_key": meeting_key})
    df['label'] = df['session_name'] + " (" + df['location'] + ")"
    return df[["session_key", "label"] ].drop_duplicates()

@st.cache_data
def fetch_laps(session_key):
    return fetch_data("laps", {"session_key": session_key})


@st.cache_data
def fetch_stints(session_key):
    return fetch_data("stints", {"session_key": session_key})


@st.cache_data
def fetch_pit_stop(session_key):
    return fetch_data("pit", {"session_key": session_key})


@st.cache_data
def fetch_drivers(session_key):
    return fetch_data("drivers", {"session_key": session_key})
