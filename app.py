import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, time, timedelta

# アプリのタイトル
st.title("残業時間入力アプリ")

# 年と月の選択
year = st.number_input("年を入力してください", min_value=2000, max_value=2100, value=datetime.now().year, step=1)
month = st.selectbox("月を選択してください", list(range(1, 13)), index=datetime.now().month - 1)

# 選択された月の日数を取得
_, num_days = calendar.monthrange(year, month)

# 曜日のリスト
weekday_names = ["月", "火", "水", "木", "金", "土", "日"]

# 日付と曜日のリストを作成
dates = []
for day in range(1, num_days + 1):
    weekday = calendar.weekday(year, month, day)
    dates.append({
        "日付": f"{year}/{month:02d}/{day:02d}",
        "曜日": weekday_names[weekday],
        "残業開始時刻": time(18, 0),
        "残業終了時刻": time(19, 0)
    })

# データフレームを作成
df = pd.DataFrame(dates)

# 編集可能なテーブルを表示
edited_df = st.data_editor(df, num_rows="dynamic")

# 残業代の計算
if st.button("残業代を計算"):
    # 時給を入力
    hourly_wage = st.number_input("時給を入力してください（円）", min_value=0, value=1500, step=100)
    # 残業代率を入力（例：1.25倍）
    overtime_rate = st.number_input("残業代率を入力してください（例：1.25）", min_value=1.0, value=1.25, step=0.05)

    total_overtime_minutes = 0

    for index, row in edited_df.iterrows():
        start = row["残業開始時刻"]
        end = row["残業終了時刻"]
        # 時間差を計算
        start_dt = datetime.combine(datetime.today(), start)
        end_dt = datetime.combine(datetime.today(), end)
        if end_dt < start_dt:
            end_dt += timedelta(days=1)  # 日をまたぐ場合の対応
        overtime = end_dt - start_dt
        total_overtime_minutes += overtime.total_seconds() / 60

    total_overtime_hours = total_overtime_minutes / 60
    overtime_pay = total_overtime_hours * hourly_wage * overtime_rate

    # 結果を表示
    st.write(f"総残業時間: {total_overtime_hours:.2f} 時間")
    st.write(f"残業代: {overtime_pay:,.0f} 円")
