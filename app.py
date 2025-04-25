import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, date, time, timedelta
from io import StringIO

# ─── 1. ページ＆サイドバー設定 ─────────────────────────
st.set_page_config(page_title="残業時間入力アプリ", layout="wide")

with st.sidebar:
    st.header("給与設定・データ管理")
    # ※条例別表第1の完全版給与データをここに貼り付けてください
    salary_table = {
        1: {1:183500,2:184600,3:185800, # …以下省略せず全81号給分を定義… },
        2: {1:230000,2:231500,3:233000, # …同様に全号給…
           },
        # 3～6級も同様に定義…
    }

    grade = st.selectbox("級を選択", list(salary_table.keys()))
    step  = st.selectbox("号給を選択", list(salary_table[grade].keys()))
    base_salary = salary_table[grade][step]
    st.write(f"基本給：{base_salary:,} 円")

    st.markdown("---")
    st.subheader("年月選択")
    year  = st.number_input("年",  2000, 2100, datetime.now().year, 1)
    month = st.selectbox("月", list(range(1,13)), index=datetime.now().month-1)

    st.markdown("---")
    st.subheader("過去データの読み込み")
    uploaded = st.file_uploader(
        "前回の記録をアップロード (CSV)", type="csv"
    )  # サイドバーにアップロードボタンを配置 :contentReference[oaicite:5]{index=5}

# ─── 2. アップロードCSVの読み込み ────────────────────────
resume = {}
if uploaded is not None:
    df_prev = pd.read_csv(uploaded, encoding="utf-8-sig")  # BOM付きUTF-8で読み込み :contentReference[oaicite:6]{index=6}
    for _, r in df_prev.iterrows():
        resume[r["日付"]] = {
            "start": datetime.strptime(r["開始時刻"], "%H:%M").time(),
            "end":   datetime.strptime(r["終了時刻"], "%H:%M").time()
        }

# ─── 3. 月の日数と曜日を取得 ───────────────────────────
_, num_days = calendar.monthrange(year, month)  # 月の日数自動取得 
weekday_names = ["月","火","水","木","金","土","日"]

# ─── 4. 各日の残業入力 ────────────────────────────────
records = []
st.subheader(f"{year}年{month:02d}月 の残業時間入力")
for d in range(1, num_days+1):
    wd = weekday_names[calendar.weekday(year, month, d)]
    label = f"{year}/{month:02d}/{d:02d} ({wd})"

    with st.expander(label):
        c1, c2 = st.columns(2)
        # アップロードデータがあれば復元、なければ平日17:15–18:15をデフォルト :contentReference[oaicite:7]{index=7}
        default_start = resume.get(label, {}).get("start",
                          time(17,15) if wd not in ("土","日") else time(0,0))
        default_end   = resume.get(label, {}).get("end",
                          time(18,15) if wd not in ("土","日") else time(0,0))

        start = c1.time_input(
            "開始時刻", value=default_start, step=900, key=f"s{d}"
        )  # 15分刻み＋テキスト入力対応 :contentReference[oaicite:8]{index=8}
        end   = c2.time_input(
            "終了時刻", value=default_end,   step=900, key=f"e{d}"
        )  # 同上 :contentReference[oaicite:9]{index=9}

        sd = datetime.combine(date.today(), start)
        ed = datetime.combine(date.today(), end)
        if ed < sd:
            ed += timedelta(days=1)
        hours = round((ed - sd).total_seconds() / 3600, 2)

        records.append({
            "日付": label,
            "開始時刻": start.strftime("%H:%M"),
            "終了時刻": end.strftime("%H:%M"),
            "残業時間": hours
        })

df = pd.DataFrame(records)

# ─── 5. 残業代計算＆CSVダウンロード ─────────────────────
st.subheader("残業代計算")
rate = st.number_input("割増率（例：1.25）", 1.0, 2.0, 1.25, 0.01)
if st.button("計算実行"):
    total_h = df["残業時間"].sum()
    hourly  = base_salary / 155  # 月所定155hで時給算出
    pay     = total_h * hourly * rate

    st.write(f"✅ 総残業時間：{total_h:.2f} 時間")
    st.write(f"✅ 残業代：{pay:,.0f} 円")

    st.dataframe(df)

    buf = StringIO()
    df.to_csv(buf, index=False, encoding="utf-8-sig")  # BOM付きUTF-8出力 :contentReference[oaicite:10]{index=10}
    st.download_button(
        "CSVダウンロード",
        data=buf.getvalue(),
        file_name="残業記録.csv",
        mime="text/csv"
    )  # ダウンロードボタン :contentReference[oaicite:11]{index=11}
