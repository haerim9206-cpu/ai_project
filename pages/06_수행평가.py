import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="인천 식당 평점 검색 시스템", layout="wide")

# 데이터 로드 함수
@st.cache_data
def load_data():
    df = pd.read_csv('food.csv', encoding='utf-8', errors='ignore')
    df.columns = df.columns.str.strip()
    # 지역명 데이터 공백 제거
    if '지역명' in df.columns:
        df['지역명'] = df['지역명'].astype(str).str.strip()
    return df

try:
    df = load_data()
    
    st.title("🍽️ 인천 지역별 식당 평점 검색 대시보드")
    st.markdown("---")
    
    # 1. 텍스트 입력으로 지역 검색 기능 구현
    st.subheader("🔍 지역명 검색")
    search_query = st.text_input(
        "검색하고 싶은 지역명을 입력해줘 (예: 연수구, 서구, 강화군, 남동구)", 
        value=""
    ).strip()
    
    st.markdown("---")
    
    if search_query:
        # 입력한 검색어가 포함된 지역 필터링 (대소문자 구분 없음)
        matched_regions = df[df['지역명'].str.contains(search_query, case=False, na=
