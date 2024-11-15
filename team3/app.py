from glob import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

df = pd.read_parquet("monthly_review_count.parquet")
df_meta = pd.read_excel("excel.xlsx")

df.review_month = df.review_month.dt.to_timestamp()

target_stores = df.store_name.unique()

st.set_page_config(layout="wide")

store_name = st.selectbox(
    '👉 리뷰 내용이 궁금한 레스토랑을 선택해주세요',
    target_stores)

store_cate = df_meta.loc[df_meta.store_name == store_name, "store_cate"].values[0]
store_location = df_meta.loc[df_meta.store_name == store_name, "store_location"].values[0]
keyword_data=df_meta.loc[df_meta.store_name == store_name, '평가 요약'].values[0]
AIcomment=df_meta.loc[df_meta.store_name == store_name, '평가'].values[0]
chef_name=df_meta.loc[df_meta.store_name == store_name, "chef_name"].values[0]

con1, con2, con3 = st.columns([0.33,0.33,0.33])

with con1:
    df_loc_target = df_meta[df_meta.store_name == store_name]
    map_data = pd.DataFrame(
        df_loc_target[["위도", "경도"]].values,
        columns=['lat', 'lon'])
    st.map(map_data)

with con2:
    st.subheader(f"🍴 {store_name}")
    st.text(f"🧑‍🍳 {chef_name} 셰프")
    st.text(f"📣 {store_cate}")
    st.text(f"📣 {store_location}")
    if str(keyword_data) not in ("NaN", "nan"):
        st.subheader("🍽️이 식당의 키워드는 이러해요!🍽️")
        st.text(f"{keyword_data}")

with con3:
    st.subheader("🖥️AI의 평가는 이러해요!🖥️")
    st.text(f"{AIcomment}")

# streamlit run app.py --server.port 80
