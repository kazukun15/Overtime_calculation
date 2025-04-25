import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, time, timedelta

# ページ設定
st.set_page_config(page_title="残業時間入力アプリ", layout="wide")

# カスタムCSSで柔らかなデザインを適用
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
        padding: 2rem;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 100%;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 残業時間入力アプリ")

# 年と月の選択
col1, col2 = st.columns(2)
with col1:
    year = st.number_input("年を入力してください", min_value=2000, max_value=2100, value=datetime.now().year, step=1)
with col2:
    month = st.selectbox("月を選択してください", list(range(1, 13)), index=datetime.now().month - 1)

# 選択された月の日数を取得
_, num_days = calendar.monthrange(year, month)

# 曜日のリスト
weekday_names = ["月", "火", "水", "木", "金", "土", "日"]

# 時間の選択肢を15分刻みで作成
def generate_time_options(start_hour=0, end_hour=23, interval_minutes=15):
    times = []
    for hour in range(start_hour, end_hour + 1):
        for minute in range(0, 60, interval_minutes):
            times.append(time(hour, minute))
    return times

time_options = generate_time_options()

# 日付ごとの入力
overtime_data = []
st.subheader(f"{year}年{month}月の残業時間入力")
for day in range(1, num_days + 1):
    weekday = calendar.weekday(year, month, day)
    date_str = f"{year}/{month:02d}/{day:02d} ({weekday_names[weekday]})"
    with st.expander(date_str):
        col1, col2 = st.columns(2)
        with col1:
            # 平日の場合、開始時刻の初期値を17:15に設定
            if weekday < 5:
                default_start_index = time_options.index(time(17, 15))
            else:
                default_start_index = 36  # 9:00
            start_time = st.selectbox(f"開始時刻 - {date_str}", time_options, index=default_
