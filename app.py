import streamlit as st  # アプリ構築用 :contentReference[oaicite:4]{index=4}
import pandas as pd     # データ操作用 :contentReference[oaicite:5]{index=5}
import requests         # Webアクセス用 
import calendar         # 月の日数取得用 
from datetime import datetime, date, time, timedelta
from io import StringIO

# ─── 1. ページ設定 ───────────────────────────────────
st.set_page_config(page_title="残業時間入力アプリ", layout="wide")  # ページタイトル＆レイアウト :contentReference[oaicite:6]{index=6}

# ─── 2. 給与表の自動取得 ───────────────────────────────
ORDINANCE_URL = "https://www.town.kamijima.lg.jp/reiki_int/reiki_honbun/r034RG00000112.html"
resp = requests.get(ORDINANCE_URL)
# HTMLページから「行政職給料表（別表第1）」を読み込む
all_tables = pd.read_html(resp.text, match="行政職給料表")  # 全ての行政職給料表テーブル抽出 :contentReference[oaicite:7]{index=7}
# 多くのテーブルがひとつのDataFrameにまとまっている場合があるため、
# 必要に応じて match や attrs 引数で特定のテーブルを絞り込む

# 取得したDataFrameを級・号給の辞書に変換
def build_salary_dict(df: pd.DataFrame) -> dict[int, dict[int, int]]:
    # 列名に「級」が含まれる列を抽出し、級リストを取得
    grade_cols = [col for col in df.columns if "級" in str(col)]
    salary_dict = {i+1: {} for i in range(len(grade_cols))}
    for _, row in df.iterrows():
        step = int(row[df.columns[0]])  # 号給は1列目
        for idx, col in enumerate(grade_cols, start=1):
            salary_dict[idx][step] = int(row[col])
    return salary_dict

salary_table = build_salary_dict(all_tables[0])  # 別表第1を辞書化 :contentReference[oaicite:8]{index=8}

# ─── 3. サイドバー：設定＆データ管理 ───────────────────
with st.sidebar:
    st.header("給与設定・データ管理")
    grade = st.selectbox("級を選択", list(salary_table.keys()))  # st.selectbox :contentReference[oaicite:9]{index=9}
    step  = st.selectbox("号給を選択", list(salary_table[grade].keys()))
    base_salary = salary_table[grade][step]
    st.write(f"基本給：{base_salary:,} 円")

    st.markdown("---")
    st.subheader("年月選択")
    year  = st.number_input("年",  2000, 2100, datetime.now().year, 1)
    month = st.selectbox("月", list(range(1,13)), index=datetime.now().month-1)

    st.markdown("---")
    st.subheader("過去データの読み込み")
    uploaded = st.file_uploader("前回の記録をアップロード (CSV)", type="csv")  # アップロード :contentReference[oaicite:10]{index=10}

# ─── 4. アップロードCSV復元 ───────────────────────────
resume: dict[str, dict[str, time]] = {}
if uploaded:
    df_prev = pd.read_csv(uploaded, encoding="utf-8-sig")  # utf-8-sig 読み込み 
    if {"日付","開始時刻","終了時刻"}.issubset(df_prev.columns):
        for _, r in df_prev.iterrows():
            resume[r["日付"]] = {
                "start": datetime.strptime(r["開始時刻"], "%H:%M").time(),
                "end":   datetime.strptime(r["終了時刻"], "%H:%M").time()
            }
    else:
        st.warning("必要な列がありません。続きから復元できませんでした。")

# ─── 5. 当月残業時間入力 ─────────────────────────────
_, num_days = calendar.monthrange(year, month)  # 日数取得 
weekday_names = ["月","火","水","木","金","土","日"]
records = []
st.subheader(f"{year}年{month:02d}月 の残業時間入力")
for d in range(1, num_days+1):
    wd = weekday_names[calendar.weekday(year, month, d)]
    label = f"{year}/{month:02d}/{d:02d} ({wd})"
    with st.expander(label):
        c1, c2 = st.columns(2)
        default_start = resume.get(label, {}).get("start", time(17,15) if wd not in ("土","日") else time(0,0))
        default_end   = resume.get(label, {}).get("end",   time(18,15) if wd not in ("土","日") else time(0,0))
        # 15分刻みテキスト入力＆ピッカー :contentReference[oaicite:11]{index=11}
        start = c1.time_input("開始時刻", value=default_start, step=900, key=f"s{d}")
        end   = c2.time_input("終了時刻", value=default_end,   step=900, key=f"e{d}")
        sd = datetime.combine(date.today(), start)
        ed = datetime.combine(date.today(), end)
        if ed < sd: ed += timedelta(days=1)
        hours = round((ed - sd).total_seconds() / 3600, 2)
        records.append({
            "日付": label,
            "開始時刻": start.strftime("%H:%M"),
            "終了時刻": end.strftime("%H:%M"),
            "残業時間": hours
        })

df = pd.DataFrame(records)

# ─── 6. 残業代計算＆CSVダウンロード ────────────────────
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
    df.to_csv(buf, index=False, encoding="utf-8-sig")  # BOM付きUTF-8 
    st.download_button(
        "CSVダウンロード",
        data=buf.getvalue(),
        file_name="残業記録.csv",
        mime="text/csv"
    )  # ダウンロードボタン :contentReference[oaicite:12]{index=12}
