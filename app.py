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
ｖ
