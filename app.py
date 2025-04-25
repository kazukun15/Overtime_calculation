import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="残業時間計算アプリ", layout="centered")

st.title("残業時間計算アプリ")

# 時間入力
col1, col2 = st.columns(2)
with col1:
    start_time = st.time_input("勤務終了時刻を入力してください", value=datetime.strptime("17:30", "%H:%M").time())
with col2:
    end_time = st.time_input("退勤時刻を入力してください", value=datetime.strptime("18:30", "%H:%M").time())

# 休憩時間入力（オプション）
break_minutes = st.number_input("残業中の休憩時間（分）", min_value=0, step=5, value=0)

# 計算ボタン
if st.button("残業時間を計算"):
    # 時間差の計算
    start_dt = datetime.combine(datetime.today(), start_time)
    end_dt = datetime.combine(datetime.today(), end_time)

    if end_dt <= start_dt:
        end_dt += timedelta(days=1)  # 日をまたぐ場合の対応

    total_overtime = (end_dt - start_dt) - timedelta(minutes=break_minutes)

    # 結果を時間・分で表示
    overtime_hours, remainder = divmod(total_overtime.seconds, 3600)
    overtime_minutes = remainder // 60

    # 結果表示
    st.success(f"残業時間：{overtime_hours}時間{overtime_minutes}分")

    # 残業代計算（例として時給を入力可能にする）
    hourly_rate = st.number_input("あなたの時給（円）を入力してください", min_value=0, step=100, value=1500)

    # 残業代は基本25%割増
    overtime_pay = (total_overtime.seconds / 3600) * hourly_rate * 1.25

    st.info(f"残業代：{overtime_pay:,.0f}円")

