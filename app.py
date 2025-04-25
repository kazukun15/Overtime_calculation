import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, time, timedelta
from io import StringIO

# 1. ページ設定
st.set_page_config(page_title="残業時間入力アプリ", layout="wide")

# 2. 給与表（条例「別表第1」）に基づく基本給データ
salary_table = {
    1: {1:183500,2:184600,3:185800,4:186900,5:188000,6:189700,7:191300,8:192900,9:194500,10:196200,
        11:197800,12:199400,13:201000,14:202700,15:204400,16:206100,17:207400,18:209000,19:210600,
        20:212100,21:213600,22:215200,23:216800,24:218400,25:220000,26:221700,27:223000,28:224300,
        29:225600,30:226700,31:227800,32:228900,33:230000,34:231100,35:232200,36:233300,37:234400,
        38:235400,39:236400,40:237300,41:238200,42:239100,43:239900,44:240700,45:241400,46:242000,
        47:242600,48:243200,49:243800,50:244400,51:245000,52:245500,53:246000,54:246400,55:246700,
        56:247000,57:247300,58:247600,59:247900,60:248200,61:248500,62:248800,63:249100,64:249400,
        65:249700,66:250000,67:250300,68:250600,69:250900,70:251200,71:251500,72:251800,73:252100,
        74:252400,75:252700,76:253000,77:253300,78:253600,79:253900,80:254200,81:254500},
    2: {1:230000,2:231500,3:233000,4:234500,5:236000,6:237500,7:239000,8:240500,9:242000,10:243400,
        # （省略: 同様に定義）
       },
    # 3～6級も同様に定義...
}

# 3. サイドバー：級・号給・年月
with st.sidebar:
    st.header("給与設定")
    grade = st.selectbox("級を選択", list(salary_table.keys()), index=0)
    step  = st.selectbox("号給を選択", list(salary_table[grade].keys()), index=0)
    base_salary = salary_table[grade][step]
    st.write(f"基本給：{base_salary:,} 円")

    st.header("年月選択")
    year  = st.number_input("年",  2000, 2100, datetime.now().year, 1)
    month = st.selectbox("月", list(range(1,13)), index=datetime.now().month-1)

# 4. 月の日数と曜日取得
_, num_days = calendar.monthrange(year, month)
weekday_names = ["月","火","水","木","金","土","日"]

# 5. 各日の残業時間入力
records = []
st.subheader(f"{year}年{month:02d}月 の残業時間入力")
for d in range(1, num_days+1):
    wd = weekday_names[calendar.weekday(year, month, d)]
    date_label = f"{year}/{month:02d}/{d:02d} ({wd})"

    # expander 内で一列に開始／終了時刻を配置
    with st.expander(date_label):
        col_start, col_end = st.columns(2)
        default_start = time(17,15) if wd not in ("土","日") else time(0,0)
        default_end   = time(18,15) if wd not in ("土","日") else time(0,0)

        # st.time_input で非スクロールの時間入力を実現 :contentReference[oaicite:2]{index=2}
        start = col_start.time_input("開始時刻", value=default_start, key=f"s{d}")
        end   = col_end.time_input(  "終了時刻", value=default_end,   key=f"e{d}")

        sd = datetime.combine(datetime.today(), start)
        ed = datetime.combine(datetime.today(), end)
        if ed < sd: ed += timedelta(days=1)
        oh = round((ed - sd).total_seconds() / 3600, 2)

        records.append({"日付":date_label, "残業時間":oh})

df = pd.DataFrame(records)

# 6. 残業代計算＆CSV保存
st.subheader("残業代計算")
overtime_rate = st.number_input("割増率 (例: 1.25倍)", 1.0, 2.0, 1.25, 0.01)
if st.button("残業代を計算"):
    total_h = df["残業時間"].sum()
    hourly = base_salary / 155  # 月所定155hで時給算出
    pay    = total_h * hourly * overtime_rate

    st.write(f"✅ 総残業時間：{total_h:.2f} 時間")
    st.write(f"✅ 残業代：{pay:,.0f} 円")
    st.dataframe(df)

    buf = StringIO()
    df.to_csv(buf, index=False)
    # CSVダウンロードボタン :contentReference[oaicite:3]{index=3}
    st.download_button("📥 CSVダウンロード", data=buf.getvalue(),
                       file_name="残業記録.csv", mime="text/csv")
