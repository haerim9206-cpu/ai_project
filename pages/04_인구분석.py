import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 앱 제목
st.title("🗺️ 행정구역별 인구 구조 분석")
st.markdown("행정구역을 선택하면 연령대별 인구수 변화를 꺾은선 그래프로 확인할 수 있습니다.")

# 데이터 로드 함수
@st.cache_data
def load_data():
    # [오류 해결 핵심] 인코딩을 cp949로 변경하여 utf-8 디코딩 에러를 해결함
    df = pd.read_csv("population.csv", encoding="cp949")
    
    # '행정구역' 컬럼에서 고유 지역 코드 제외하고 이름만 정리
    df['행정구역_표시'] = df['행정구역'].str.split(' \(').str[0]
    return df

try:
    df = load_data()

    # 사이드바 또는 메인 화면에서 행정구역 선택
    target_region = st.selectbox("분석할 행정구역을 선택하세요", df['행정구역_표시'].unique())

    # 선택한 행정구역의 데이터 추출
    selected_row = df[df['행정구역_표시'] == target_region].iloc[0]

    # 그래프에 그릴 연령대 컬럼 정의 (X축 라벨로 사용)
    age_groups = [
        "0~9세", "10~19세", "20~29세", "30~39세", "40~49세", 
        "50~59세", "60~69세", "70~79세", "80~89세", "90~99세", "100세 이상"
    ]

    # 데이터 매핑 (숫자 데이터 형식으로 변환, 콤마 제거)
    total_population = []
    male_population = []
    female_population = []

    for age in age_groups:
        # 총인구, 남, 여 컬럼명 매칭하여 값 가져오기
        tot_val = int(str(selected_row[f"2026년04월_거주자_{age}"]).replace(',', ''))
        male_val = int(str(selected_row[f"2026년04월_남_거주자_{age}"]).replace(',', ''))
        female_val = int(str(selected_row[f"2026년04월_여_거주자_{age}"]).replace(',', ''))
        
        total_population.append(tot_val)
        male_population.append(male_val)
        female_population.append(female_val)

    # Plotly를 이용한 인터랙티브 꺾은선 그래프 그리기
    fig = go.Figure()

    # 꺾은선 그래프 추가 (파스텔톤 연보라색: #B39DDB, 마우스 오버 커스텀 툴팁 설정)
    fig.add_trace(go.Scatter(
        x=age_groups, 
        y=total_population, 
        mode='lines+markers',
        name='총 인구수',
        line=dict(color='#B39DDB', width=4),
        marker=dict(size=8),
        hovertemplate='<b>%{x}</b><br>인구수: %{y:,}명<extra></extra>' # 마우스 올리면 정확한 값 팝업
    ))

    # 축 이름 변경 반영 (가로축: age, 세로축: population, 바탕색: 파스텔톤 연두색 #EBF7E3)
    fig.update_layout(
        title=dict(
            text=f"[{target_region}] 연령별 인구수 추이",
            font=dict(size=18)
        ),
        xaxis=dict(
            title="age",  # 가로축 이름 변경
            titlefont=dict(size=14, color='#333333'),
            gridcolor='rgba(150, 150, 150, 0.2)'
        ),
        yaxis=dict(
            title="population",  # 세로축 이름 변경
            titlefont=dict(size=1
