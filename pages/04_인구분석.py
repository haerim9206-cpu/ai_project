import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import urllib.request

# 1. 스트림릿 클라우드 한글 깨짐 방지를 위한 폰트 다운로드 설정
@st.cache_data
def load_korean_font():
    font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
    font_path = "NanumGothic.ttf"
    
    # 폰트 파일이 로컬(서버)에 없으면 다운로드
    if not os.path.exists(font_path):
        urllib.request.urlretrieve(font_url, font_path)
    
    # Matplotlib에 폰트 등록 및 설정
    fm.font_manager.addfont(font_path)
    font_prop = fm.FontProperties(fname=font_path)
    plt.rc('font', family=font_prop.get_name())
    plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지

# 폰트 로드 및 적용
load_korean_font()

# 앱 상단 제목
st.title("📊 서울시 행정구역 인구수 분석")
st.markdown("행정구역을 선택하면 연령대별 인구수 추이를 꺾은선 그래프로 확인할 수 있습니다.")

# 2. 데이터 로드 함수
@st.cache_data
def load_data():
    # 제공된 population.csv 파일을 읽어옴 (app.py와 같은 폴더에 있어야 함)
    df = pd.read_csv("population.csv", encoding="utf-8")
    
    # '행정구역' 컬럼에서 행정기관코드 생략하고 이름만 깔끔하게 정리
    # 예: "서울특별시 종로구 (1111000000)" -> "서울특별시 종로구"
    df['행정구역_표시'] = df['행정구역'].str.split(' \(').str[0]
    return df

try:
    df = load_data()

    # 3. 행정구역 선택 셀렉트박스
    target_region = st.selectbox("분석할 행정구역을 선택하세요", df['행정구역_표시'].unique())

    # 선택한 행정구역의 행 데이터 가져오기
    selected_row = df[df['행정구역_표시'] == target_region].iloc[0]

    # 4. X축에 사용할 연령대 라벨 정의
    age_groups = [
        "0~9세", "10~19세", "20~29세", "30~39세", "40~49세", 
        "50~59세", "60~69세", "70~79세", "80~89세", "90~99세", "100세 이상"
    ]

    # 각 연령대별 총 인구수 데이터 추출 및 전처리 (쉼표 제거 후 숫자로 변환)
    total_population = []
    for age in age_groups:
        col_name = f"2026년04월_거주자_{age}"
        val = int(str(selected_row[col_name]).replace(',', ''))
        total_population.append(val)

    # 5. 그래프 그리기 (파스텔톤 연두색 배경 + 파스텔톤 연보라색 선)
    fig, ax = plt.subplots(figsize=(10, 6))

    # 그래프 배경색 설정 (파스텔톤 연두색: #EBF7E3)
    fig.patch.set_facecolor('#EBF7E3')
    ax.set_facecolor('#EBF7E3')

    # 꺾은선 그래프 그리기 (파스텔톤 연보라색 선: #B39DDB, 마커 포함)
    ax.plot(age_groups, total_population, marker='o', markersize=6, linewidth=3, color='#B39DDB', label='총 인구수')

    # 그래프 세부 스타일 지정
    ax.set_title("서울시 행정구역 인구수", fontsize=18, fontweight='bold', pad=20, color='#333333')
    ax.set_xlabel("나이", fontsize=12, labelpad=10)
    ax.set_ylabel("인구수", fontsize=12, labelpad=10)
    
    # 그리드 선 스타일 및 색상 설정
    ax.grid(True, linestyle='--', alpha=0.5, color='#999999')
    ax.legend(loc='upper right')

    # Y축 천 단위 콤마 표기
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

    # 스트림릿 웹 화면에 그래프 출력
    st.pyplot(fig)

    # 데이터 표도 함께 출력
    st.subheader("📋 선택 구역 상세 데이터")
    info_df = pd.DataFrame({
        "나이(연령대)": age_groups,
        "인구수(명)": [f"{x:,}" for x in total_population]
    })
    st.dataframe(info_df, use_container_width=True)

except FileNotFoundError:
    st.error("⚠️ `population.csv` 파일을 찾을 수 없습니다. 대시보드 파일과 같은 디렉토리에 넣어주세요.")
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
