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
            start_time = st.selectbox(f"開始時刻 - {date_str}", time_options, index=default_start_index, key=f"start_{day}")
        with col2:
            end_time = st.selectbox(f"終了時刻 - {date_str}", time_options, index=default_start_index + 4, key=f"end_{day}")
        # 時間差を計算
        start_dt = datetime.combine(datetime.today(), start_time)
        end_dt = datetime.combine(datetime.today(), end_time)
        if end_dt < start_dt:
            end_dt += timedelta(days=1)  # 日をまたぐ場合の対応
        overtime = end_dt - start_dt
        overtime_hours = overtime.total_seconds() / 3600
        overtime_data.append({
            "日付": f"{year}/{month:02d}/{day:02d}",
            "曜日": weekday_names[weekday],
            "開始時刻": start_time.strftime("%H:%M"),
            "終了時刻": end_time.strftime("%H:%M"),
            "残業時間（時間）": round(overtime_hours, 2)
        })

# データフレームを作成
df = pd.DataFrame(overtime_data)

# 残業代の計算
st.subheader("💰 残業代の計算")
hourly_wage = st.number_input("時給を入力してください（円）", min_value=0, value=1500, step=100)
overtime_rate = st.number_input("残業代率を入力してください（例：1.25）", min_value=1.0, value=1.25, step=0.05)

if st.button("残業代を計算"):
    total_overtime_hours = df["残業時間（時間）"].sum()
    overtime_pay = total_overtime_hours * hourly_wage * overtime_rate

    # 結果を表示
    st.write(f"総残業時間: {total_overtime_hours:.2f} 時間")
    st.write(f"残業代: {overtime_pay:,.0f} 円")

    # 詳細なデータを表示
    st.dataframe(df)
