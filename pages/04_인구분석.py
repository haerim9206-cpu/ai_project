import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import urllib.request

# 1. 스트림릿 클라우드 한글 깨짐 방지를 위한 안전한 폰트 설정
@st.cache_data
def load_korean_font():
    font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
    font_path = "NanumGothic.ttf"
    
    if not os.path.exists(font_path):
        urllib.request.urlretrieve(font_url, font_path)
    
    # Matplotlib 버전에 상관없이 안전하게 폰트 객체 추가하기
    font_entry = fm.FontEntry(fname=font_path, name='NanumGothic')
    fm.font_manager.ttflist.insert(0, font_entry)
    
    plt.rc('font', family='NanumGothic')
    plt.rcParams['axes.unicode_minus'] = False # 마이너스 깨짐 방지

load_korean_font()

# 앱 제목
st.title("📊 서울시 행정구역 인구수 분석")
st.markdown("특정 나이대를 선택하면, 해당 연령대 인구가 가장 많은 **상위 10개 행정구**를 뽑아 연령별 인구 추이를 비교합니다.")

# 2. 데이터 로드 및 전처리
@st.cache_data
def load_data():
    df = pd.read_csv("population.csv", encoding="utf-8")
    df['행정구역_표시'] = df['행정구역'].str.split(' \(').str[0]
    return df

try:
    df = load_data()

    # 기준이 될 10세 간격 나이대 목록
    age_groups = [
        "0~9세", "10~19세", "20~29세", "30~39세", "40~49세", 
        "50~59세", "60~69세", "70~79세", "80~89세", "90~99세", "100세 이상"
    ]

    # 3. 사이드바나 메인화면에서 순위를 매길 기준 나이대 선택
    selected_age = st.selectbox("기준이 될 나이대를 선택하세요 (이 나이대가 가장 많은 구 TOP 10 추출)", age_groups, index=2)

    # 데이터 수치화 (숫자 안의 쉼표 제거 후 int 변환)
    # 각 행정구별로 그래프에 그릴 연령대 데이터를 미리 변환해둠
    for age in age_groups:
        df[f'num_{age}'] = df[f"2026년04월_거주자_{age}"].astype(str).str.replace(',', '').astype(int)

    # 4. 선택한 나이대 인구수가 가장 많은 상위 10개 행정구 필터링
    # (전국 데이터가 섞여있을 수 있으므로 '전체', '총계' 등 행정구가 아닌 행은 제외하는 필터링 포함)
    top10_df = df[~df['행정구역_표시'].str.contains('전국|계$|인구')].sort_values(by=f'num_{selected_age}', ascending=False).head(10)

    # 5. 그래프 그리기 (파스텔톤 연두색 배경)
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # 바탕색 설정 (파스텔톤 연두색계열)
    fig.patch.set_facecolor('#EBF7E3')
    ax.set_facecolor('#EBF7E3')

    # 10개의 구를 구분하기 위한 파스텔톤 연보라~자주색 중심의 색상 팔레트 설정
    # 요청하신 연보라색(#
 
