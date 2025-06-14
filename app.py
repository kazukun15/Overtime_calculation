import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, date, time, timedelta
from io import StringIO

# ─── 1. ページ設定 ───────────────────────────────────
st.set_page_config(page_title="残業時間入力アプリ", layout="wide")  # ページタイトル＆レイアウト設定 :contentReference[oaicite:3]{index=3}

# ─── 2. サイドバー：給与設定・データ管理 ─────────────────
with st.sidebar:
    st.header("給与設定・データ管理")

    # ◉ 条例別表第1：行政職給料表（1級～6級×81号給）完全版
    salary_table = {
        1: {1:183500,2:184600,3:185800,4:186900,5:188000,6:189700,7:191300,8:192900,9:194500,10:196200,
            11:197800,12:199400,13:201000,14:202700,15:204400,16:206100,17:207400,18:209000,19:210600,20:212100,
            21:213600,22:215200,23:216800,24:218400,25:220000,26:221700,27:223000,28:224300,29:225600,30:226700,
            31:227800,32:228900,33:230000,34:231100,35:232200,36:233300,37:234400,38:235400,39:236400,40:237300,
            41:238200,42:239100,43:239900,44:240700,45:241400,46:242000,47:242600,48:243200,49:243800,50:244400,
            51:245000,52:245500,53:246000,54:246400,55:246700,56:247000,57:247300,58:247600,59:247900,60:248200,
            61:248500,62:248800,63:249100,64:249400,65:249700,66:250000,67:250300,68:250600,69:250900,70:251200,
            71:251500,72:251800,73:252100,74:252400,75:252700,76:253000,77:253300,78:253600,79:253900,80:254200,
            81:254500},
        2: {1:230000,2:231500,3:233000,4:234500,5:236000,6:237500,7:239000,8:240500,9:242000,10:243400,
            11:244800,12:246200,13:247400,14:248600,15:249800,16:251000,17:252100,18:253200,19:254300,20:255400,
            21:256400,22:257400,23:258400,24:259400,25:260400,26:261300,27:262200,28:263100,29:263900,30:264700,
            31:265500,32:266300,33:267000,34:267800,35:268600,36:269300,37:270000,38:270800,39:271600,40:272300,
            41:273000,42:273800,43:274600,44:275300,45:276000,46:276700,47:277400,48:278100,49:278800,50:279500,
            51:280200,52:280900,53:281500,54:282200,55:282800,56:283500,57:284100,58:284800,59:285400,60:286100,
            61:286700,62:287400,63:288000,64:288500,65:289000,66:289600,67:290100,68:290700,69:291200,70:291700,
            71:292300,72:292900,73:293400,74:293900,75:294300,76:294600,77:294800,78:295100,79:295300,80:295600,
            81:295800},
        3: {1:261300,2:262300,3:263300,4:264300,5:265300,6:266300,7:267300,8:268300,9:269300,10:270300,
            11:271300,12:272300,13:273300,14:274300,15:275300,16:276400,17:277400,18:278700,19:280000,20:281200,
            21:282500,22:283800,23:285000,24:286200,25:287300,26:288500,27:289800,28:291100,29:292400,30:293400,
            31:294400,32:295500,33:296600,34:297800,35:298900,36:300100,37:301300,38:302600,39:303900,40:305200,
            41:306500,42:307800,43:309100,44:310400,45:311700,46:313000,47:314300,48:315400,49:316300,50:317600,
            51:318900,52:320200,53:321400,54:322700,55:323900,56:325100,57:326400,58:327500,59:328600,60:329700,
            61:330400,62:331300,63:332000,64:332800,65:333600,66:334000,67:334600,68:335300,69:336100,70:336800,
            71:337500,72:338100,73:338600,74:339200,75:339700,76:340300,77:340600,78:341100,79:341500,80:341900,
            81:342300},
        4: {1:287300,2:288900,3:290400,4:291900,5:293400,6:294900,7:296300,8:297600,9:298800,10:300300,
            11:301800,12:303200,13:304600,14:305700,15:306700,16:307900,17:309100,18:310700,19:312300,20:313900,
            21:315400,22:317000,23:318600,24:320200,25:321700,26:323400,27:325000,28:326600,29:328000,30:329700,
            31:331400,32:333000,33:334200,34:336100,35:337800,36:339400,37:340900,38:342500,39:344100,40:345700,
            41:347400,42:349200,43:351000,44:352800,45:354300,46:355700,47:357100,48:358500,49:360000,50:360800,
            51:361800,52:362800,53:363700,54:364800,55:365700,56:366700,57:367600,58:368300,59:369000,60:369600,
            61:370000,62:370600,63:371300,64:372000,65:372300,66:373000,67:373700,68:374300,69:374600,70:375100,
            71:375700,72:376300,73:376600,74:377200,75:377900,76:378500,77:378900,78:379400,79:380000,80:380500,
            81:381000},
        5: {1:309800,2:311500,3:313200,4:314700,5:316100,6:317400,7:318700,8:320000,9:321300,10:323100,
            11:324900,12:326600,13:328300,14:330000,15:331700,16:333400,17:335000,18:336700,19:338400,20:340000,
            21:341500,22:343100,23:344700,24:346200,25:347600,26:349300,27:350900,28:352500,29:353700,30:355200,
            31:356700,32:358200,33:359900,34:361700,35:363400,36:365100,37:366500,38:367800,39:369000,40:370400,
            41:371500,42:372400,43:373400,44:374500,45:375300,46:376200,47:377100,48:377900,49:378700,50:379500,
            51:380300,52:381000,53:381700,54:382400,55:383100,56:383800,57:384300,58:384900,59:385500,60:386200,
            61:386600,62:387200,63:387800,64:388300,65:388700,66:389300,67:389900,68:390400,69:390800,70:391300,
            71:391800,72:392400,73:392700,74:393100,75:393500,76:393900,77:394200,78:394500,79:394800,80:395000,
            81:395200},
        6: {1:335000,2:336900,3:338700,4:340500,5:342200,6:343900,7:345500,8:347200,9:348800,10:350500,
            11:352100,12:353700,13:355200,14:356900,15:358500,16:360100,17:361700,18:363500,19:365000,20:366600,
            21:368000,22:369600,23:371200,24:372700,25:374600,26:376500,27:378400,28:380200,29:381700,30:383500,
            31:385200,32:386800,33:388500,34:389900,35:391300,36:392700,37:394100,38:395300,39:396500,40:397500,
            41:398600,42:399800,43:400900,44:402000,45:402700,46:403400,47:404100,48:404800,49:405400,50:406000,
            51:406500,52:406900,53:407300,54:407500,55:407800,56:408100,57:408400,58:408700,59:409000,60:409300,
            61:409500,62:409800,63:410100,64:410400,65:410600,66:410900,67:411200,68:411500,69:411700,70:412000,
            71:412300,72:412500,73:412700,74:413000,75:413300,76:413500,77:413700,78:414000,79:414300,80:414500,
            81:414700}
    }  # 正確な条例準拠給与表

    grade = st.selectbox("級を選択", list(salary_table.keys()))
    step  = st.selectbox("号給を選択", list(salary_table[grade].keys()))
    base_salary = salary_table[grade][step]
    st.write(f"基本給：{base_salary:,} 円")  # 基本給表示

    st.markdown("---")
    st.subheader("年月選択")
    year  = st.number_input("年",  2000, 2100, datetime.now().year, 1)  # 年選択&#8203;:contentReference[oaicite:4]{index=4}
    month = st.selectbox("月", list(range(1,13)), index=datetime.now().month-1)  # 月選択

    st.markdown("---")
    st.subheader("過去データの読み込み")
    uploaded = st.file_uploader("前回の記録をアップロード (CSV)", type="csv")  # CSVアップロード&#8203;:contentReference[oaicite:5]{index=5}

# 3. アップロードCSVの読み込みと復元
resume = {}
if uploaded is not None:
    df_prev = pd.read_csv(uploaded, encoding="utf-8-sig")  # UTF-8 BOM付きで読み込み
    if {"日付","開始時刻","終了時刻"}.issubset(df_prev.columns):
        for _, r in df_prev.iterrows():
            resume[r["日付"]] = {
                "start": datetime.strptime(r["開始時刻"], "%H:%M").time(),
                "end":   datetime.strptime(r["終了時刻"], "%H:%M").time()
            }
    else:
        st.warning("CSV に必要な列がありません。復元をスキップします。")

# 4. 残業時間入力
_, num_days = calendar.monthrange(year, month)  # 月の日数取得
weekday_names = ["月","火","水","木","金","土","日"]
records = []
st.subheader(f"{year}年{month:02d}月 の残業時間入力")
for d in range(1, num_days+1):
    wd = weekday_names[calendar.weekday(year, month, d)]
    label = f"{year}/{month:02d}/{d:02d} ({wd})"
    with st.expander(label):
        c1, c2 = st.columns(2)
        default_start = resume.get(label, {}).get("start",
                          time(17,15) if wd not in ("土","日") else time(0,0))
        default_end   = resume.get(label, {}).get("end",
                          time(18,15) if wd not in ("土","日") else time(0,0))
        # 時刻ピッカー＋テキスト入力（15分刻み）&#8203;:contentReference[oaicite:6]{index=6}
        start = c1.time_input("開始時刻", value=default_start, step=900, key=f"s{d}")
        end   = c2.time_input("終了時刻", value=default_end,   step=900, key=f"e{d}")

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

# 5. DataFrame化
df = pd.DataFrame(records)

# 6. 残業代計算＆CSVダウンロード
st.subheader("残業代計算")
rate = st.number_input("割増率（例：1.25）", 1.0, 2.0, 1.25, 0.01)  # 割増率入力&#8203;:contentReference[oaicite:7]{index=7}
if st.button("計算実行"):
    total_h = df["残業時間"].sum()
    hourly  = base_salary / 155  # 時給算出
    pay     = total_h * hourly * rate

    st.write(f"✅ 総残業時間：{total_h:.2f} 時間")
    st.write(f"✅ 残業代：{pay:,.0f} 円")
    st.dataframe(df)  # DataFrame 表示&#8203;:contentReference[oaicite:8]{index=8}

    buf = StringIO()
    df.to_csv(buf, index=False, encoding="utf-8-sig")  # UTF-8 BOM付き出力
    st.download_button(
        "CSVダウンロード",
        data=buf.getvalue(),
        file_name="残業記録.csv",
        mime="text/csv"
    )  # ダウンロード&#8203;:contentReference[oaicite:9]{index=9}
