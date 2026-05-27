import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 0. 페이지 설정
st.set_page_config(page_title="서울 역대 기온 분석기", layout="wide")

st.title("🌡️ 서울 역대 날짜별 기온 변화 분석기")
st.markdown("1907년부터 서울의 기온 데이터를 기반으로, 특정 날짜의 연도별 최고/최저 기온 추이를 분석합니다.")

# 1. 데이터 로드 및 전처리 함수
@st.cache_data
def load_data():
    # 데이터 불러오기 (인코딩 에러 방지 위해 cp949 설정)
    df = pd.read_csv('seoul.csv', encoding='cp949')
    
    # 공백이나 탭 문자 제거 (\t1907-10-01 형식 방지)
    df['날짜'] = df['날짜'].astype(str).str.strip()
    
    # 날짜 데이터 타입을 datetime으로 변환 (변환 오류는 NaN 처리)
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    
    # 결측치 제거 (날짜나 기온이 없는 행 제외)
    df = df.dropna(subset=['날짜', '최고기온(℃)', '최저기온(℃)'])
    
    # 월, 일, 연도 컬럼 생성
    df['연도'] = df['날짜'].dt.year
    df['월'] = df['날짜'].dt.month
    df['일'] = df['날짜'].dt.day
    
    return df

try:
    df = load_data()

    # 2. 사이드바 - 월/일 선택 UI
    st.sidebar.header("🗓️ 분석하고 싶은 날짜 선택")
    
    selected_month = st.sidebar.selectbox("월(Month)을 선택하세요", sorted(df['월'].unique()), index=4) # 기본값 5월
    
    # 선택한 월에 존재하는 일(Day)만 필터링해서 보여주기
    available_days = sorted(df[df['월'] == selected_month]['일'].unique())
    selected_day = st.sidebar.selectbox("일(Day)을 선택하세요", available_days, index=26) # 기본값 27일

    # 3. 데이터 필터링
    filtered_df = df[(df['월'] == selected_month) & (df['일'] == selected_day)].sort_values(by='연도')

    # 4. 시각화 및 결과 출력
    if not filtered_df.empty:
        st.subheader(f"📊 역대 {selected_month}월 {selected_day}일 기온 변화 그래프")
        
        # Plotly를 이용한 꺾은선 그래프 생성
        fig = go.Figure()
        
        # 최고기온 (연분홍색 - Soft Pink: #FFB6C1)
        fig.add_trace(go.Scatter(
            x=filtered_df['연도'], 
            y=filtered_df['최고기온(℃)'],
            mode='lines+markers',
            name='최고기온 (℃)',
            line=dict(color='#FFB6C1', width=2.5),
            marker=dict(size=5)
        ))
        
        # 최저기온 (연파란색 - Light Sky Blue: #87CEFA)
        fig.add_trace(go.Scatter(
            x=filtered_df['연도'], 
            y=filtered_df['최저기온(℃)'],
            mode='lines+markers',
            name='최저기온 (℃)',
            line=dict(color='#87CEFA', width=2.5),
            marker=dict(size=5)
        ))
        
        # 그래프 레이아웃 스타일 설정
        fig.update_layout(
            xaxis_title="연도 (Year)",
            yaxis_title="기온 (℃)",
            hovermode="x unified", # 마우스를 올리면 같은 연도의 최고/최저 기온이 함께 보임
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=40, b=40),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        # 그리드 라인 설정
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#F0F0F0')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#F0F0F0')
        
        # 스트림릿 화면에 그래프 그리기
        st.plotly_chart(fig, use_container_width=True)
        
        # 간단한 요약 데이터 요약창
        col1, col2, col3 = st.columns(3)
        with col1:
            max_row = filtered_df.loc[filtered_df['최고기온(℃)'].idxmax()]
            st.metric(label=f"역대 가장 더웠던 {selected_month}/{selected_day}", value=f"{max_row['최고기온(℃)']} ℃", delta=f"{int(max_row['연도'])}년")
        with col2:
            min_row = filtered_df.loc[filtered_df['최저기온(℃)'].idxmin()]
            st.metric(label=f"역대 가장 추웠던 {selected_month}/{selected_day}", value=f"{min_row['최저기온(℃)']} ℃", delta=f"{int(min_row['연도'])}년", delta_color="inverse")
        with col3:
            st.metric(label="총 데이터 연도 수", value=f"{len(filtered_df)}개 연도")

    else:
        st.warning("선택한 날짜에 해당하는 데이터가 존재하지 않습니다.")

except FileNotFoundError:
    st.error("❌ `seoul.csv` 파일을 찾을 수 없습니다. 파이썬 스크립트(`app.py`)와 같은 폴더에 파일을 넣어주세요.")
