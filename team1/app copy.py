from glob import glob

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# 데이터 불러오기
df = pd.read_parquet("monthly_review_count.parquet")
df.review_month = df.review_month.dt.to_timestamp()

# 고유한 가게 이름 리스트 생성
target_stores = df.store_name.unique()

# 사용자가 선택한 가게 이름
store_name = st.selectbox(
    '리뷰 내용이 궁금한 레스토랑을 선택해주세요',
    target_stores)

# 선택된 가게의 데이터 필터링
filtered_df = df[df.store_name == store_name]

# 히스토그램 생성
fig = plt.figure()
plt.hist(filtered_df['review_month'], bins=12, edgecolor='black')
plt.xlabel('Month')
plt.ylabel('Review count')
plt.axvline(x=target_date, color='r', linestyle='--', label='2024-09-17')
plt.xticks(rotation=20)
st.pyplot(fig)

# streamlit run app.py --server.port 80
