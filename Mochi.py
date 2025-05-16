import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import pandas as pd
import plotly.express as plt

# Define scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Authorize credentials (point to your downloaded JSON key)
creds = ServiceAccountCredentials.from_json_keyfile_name("mochidatasaved-d6d2e912e503.json", scope)
client = gspread.authorize(creds)

spreadsheet_url = "https://docs.google.com/spreadsheets/d/1HZMeuQ0il4EsWO4cozLUuBRv-CYVqS9S_O1UneHJBIo/edit?usp=sharing"
working_sheet = client.open_by_url(spreadsheet_url).worksheet("Sheet1")

## Design the UI

# collect user mood
st.set_page_config(page_title="Mood Log", layout="centered")
st.title("How you feel today?")
st.subheader("Mark your mood")



# Options
opt_mood = st.selectbox("Select your mood:", ["😊: Joyful", "😠: Frustrating",  "😕: Confusing", "🎉: Excellent"])
opt_note = st.text_input("Anything you want to tell us?")

submitted = False
# Log a mod
if st.button("Mark your mood"):
    opt_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_new = [opt_timestamp, opt_mood, opt_note]

    working_sheet.append_row(data_new)
    st.success("We have logged your feedbacks!")
    submitted = True


## Visualize the mood
def load_today_data():
    record = working_sheet.get_all_records()
    df = pd.DataFrame(record)
    df['timestamp'] = pd.to_datetime(df["timestamp"])
    df['date'] = df['timestamp'].dt.date
    df['mood'] = df['mood']
    return df


if submitted:
    st.subheader("This is how people feel today:")

    saved_data = load_today_data()
    today = datetime.date.today()
    today_data = saved_data[saved_data['date'] == today]


    # Count the mood
    if not today_data.empty:
        mood_count = today_data["mood"].value_counts().reset_index()
        mood_count.columns = ['Mood', 'Value']

        fig = plt.bar(mood_count, x = "Mood", y = "Value", title = f"Mood summary for {today}")

        st.plotly_chart(fig)
    else:
        st.write("There is no mood today")


