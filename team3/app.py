from glob import glob

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

df = pd.read_parquet("monthly_review_count.parquet")
df_meta = pd.read_parquet("df_meta.parquet")
df_loc = pd.read_excel("excel2.xlsx")

df.review_month = df.review_month.dt.to_timestamp()

target_stores = df.store_name.unique()


store_name = st.selectbox(
    '리뷰 내용이 궁금한 레스토랑을 선택해주세요',
    target_stores)


store_cate = df_meta.loc[df_meta.store_name == store_name, "store_cate"].values[0]
store_location = df_meta.loc[df_meta.store_name == store_name, "store_location"].values[0]

con1, con2 = st.columns([0.5,0.5])

with con1:
    df_loc_target = df_loc[df_loc.store_name == store_name]
    map_data = pd.DataFrame(
        # [[37.4900861966504, 127.01953478052]],
        df_loc_target[["위도", "경도"]].values,
        columns=['lat', 'lon'])
    st.map(map_data)

with con2:
    st.subheader(f"식당 이름: {store_name}")
    st.text(f"식당 종류: {store_cate}")
    st.text(f"식당 위치: {store_location}")

# streamlit run app.py --server.port 80
