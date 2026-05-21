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
    
    # 폰트 파일이 로컬(서버)에 없으면 다운로드
    if not os.path.exists(font_path):
        urllib.request.urlretrieve(font_url, font_path)
    
    # Matplotlib 버전에 상관없이 안전하게 폰트 객체 추가하기 (오류 해결)
    font_entry = fm.FontEntry(fname=font_path, name='NanumGothic')
    fm.font_manager.ttflist.insert(0, font_entry)
    
    plt.rc('font', family='NanumGothic')
    plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지

# 폰트 로드 및 적용
load_korean_font()

# 앱 제목
st.title("📊 서울시 행정구역 인구수 분석")
st.markdown("특정 나이대를 선택하면, 해당 연령대 인구가 가장 많은 **상위 10개 행정구역**을 뽑아 연령별 인구 추이를 꺾은선으로 비교합니다.")

# 2. 데이터 로드 및 전처리 함수
@st.cache_data
def load_data():
    # 제공된 population.csv 파일을 읽어옴 (app.py와 같은 폴더에 있어야 함)
    df = pd.read_csv("population.csv", encoding="utf-8")
    
    # '행정구역' 컬럼에서 행정기관코드 생략하고 이름만 정리
    # 예: "서울특별시 종로구 (1111000000)" -> "서울특별시 종로구"
    df['행정구역_표시'] = df['행정구역'].str.split(' \(').str[0]
    return df

try:
    df = load_data()

    # 기준이 될 10세 간격 나이대 목록
    age_groups = [
        "0~9세", "10~19세", "20~29세", "30~39세", "40~49세", 
        "50~59세", "60~69세", "70~79세", "80~89세", "90~99세", "100세 이상"
    ]

    # 3. 사이드바 또는 메인화면에서 순위를 매길 기준 나이
