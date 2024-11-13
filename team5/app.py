import pandas as pd
import streamlit as st

df_meta = pd.read_parquet("df_meta.parquet")



# Streamlit 세션 상태에서 현재 페이지를 추적하기 위한 초기 설정
if 'page' not in st.session_state:
    st.session_state['page'] = 'main'

# 다른 페이지로 이동하는 함수
def navigate_to(page):
    st.session_state['page'] = page
    st.rerun()

# 메인 페이지 내용 정의
def main_page():
    st.title('써비쓰')
    
    with st.expander(label="요리하는돌아이", expanded=True):
        
        st.image("https://i.ytimg.com/vi/twWD41zbMRk/hqdefault.jpg")
        if st.button('이동1'):
            navigate_to('sub1')

    with st.expander(label="정지선", expanded=True):
        
        st.image("https://pds.joongang.co.kr/news/component/htmlphoto_mmdata/202411/09/7814afd8-4d59-43a2-b0df-dd0ef9aec9bc.jpg")
        if st.button('이동2'):
            navigate_to('sub2')
    

# 서브 페이지 내용 정의
def sub_page(sub_count):
    st.title('서브 페이지')
    st.write(f'여기는 서브 페이지 {sub_count}입니다.')
    if st.button('메인 페이지로 돌아가기'):
        navigate_to('main')

# 페이지 네비게이션 로직
if st.session_state['page'] == 'main':
    main_page()
elif st.session_state['page'] == 'sub1':
    sub_page(1)
elif st.session_state['page'] == 'sub2':
    sub_page(2)
                        


