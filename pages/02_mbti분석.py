import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="Global MBTI Explorer", layout="wide")

@st.cache_data
def load_data():
    # 파일명이 업로드한 파일과 일치해야 해
    df = pd.read_csv('countriesMBTI_16types.csv')
    return df

try:
    df = load_data()

    st.title("🌍 국가별 MBTI 유형 분포 확인하기")
    st.markdown("국가를 선택하면 해당 국가의 MBTI 비율을 확인할 수 있어. **1위 유형은 빨간색**으로 표시돼!")

    # 국가 선택 셀렉트박스
    countries = df['Country'].unique()
    selected_country = st.selectbox("분석할 국가를 선택해줘:", countries)

    # 선택된 국가 데이터 추출 및 재구조화
    country_data = df[df['Country'] == selected_country].drop(columns=['Country']).T
    country_data.columns = ['Percentage']
    country_data = country_data.sort_values(by='Percentage', ascending=False).reset_index()
    country_data.columns = ['MBTI', 'Percentage']

    # 색상 설정: 1등은 빨간색, 나머지는 파란색 그라데이션 느낌
    # Plotly의 Blues 스케일을 활용해서 1등 제외 나머지에 적용
    colors = ['#EF553B'] + px.colors.sequential.Blues_r[1:len(country_data)]
    # 만약 데이터 개수보다 색상 리스트가 부족하면 반복해서 채움
    if len(colors) < len(country_data):
        colors = colors + [px.colors.sequential.Blues_r[-1]] * (len(country_data) - len(colors))

    # 차트 생성
    fig = go.Figure(go.Bar(
        x=country_data['MBTI'],
        y=country_data['Percentage'],
        marker_color=colors[:len(country_data)],
        hovertemplate='<b>%{x}</b><br>비율: %{y:.2%}<extra></extra>'
    ))

    fig.update_layout(
        title=f"<b>{selected_country}</b>의 MBTI 유형별 비율",
        xaxis_title="MBTI 유형",
        yaxis_title="비율",
        yaxis_tickformat='.1%',
        template="plotly_white",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    # 상세 데이터 표
    with st.expander("상세 데이터 보기"):
        st.dataframe(country_data.style.format({'Percentage': '{:.2%}'}))

except FileNotFoundError:
    st.error("데이터 파일을 찾을 수 없어. `countriesMBTI_16types.csv` 파일이 같은 경로에 있는지 확인해줘.")
