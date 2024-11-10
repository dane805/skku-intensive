from glob import glob

import streamlit as st
from PIL import Image

clouod_jpgs = glob("../outputs/*_cloud.jpg")

target_stores = [path.split("/")[-1].split("_")[0] for path in clouod_jpgs]
store_name = st.selectbox(
    '리뷰 내용이 궁금한 레스토랑을 선택해주세요',
    target_stores)

# st.write('당신이 좋아하는 동물은 :', animal)
img = Image.open(f'../outputs/{store_name}_cloud.jpg')
	# 경로에 있는 이미지 파일을 통해 변수 저장
st.image(img)
# streamlit run streamlit_test.py --server.port 80