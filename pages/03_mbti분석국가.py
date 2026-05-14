import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="Global MBTI Ranking", layout="wide")

@st.cache_data
def load_data():
    # 파일 경로가 업로드한 파일명과 일치해야 함
    df = pd.read_csv('countriesMBTI_16types.csv')
    return df

try:
    df = load_data()

    st.title("📊 MBTI 유형별 국가 순위 확인하기")
    st.markdown("특정 MBTI를 선택하면 어떤 나라에 그 유형이 가장 많은지 확인할 수 있어. **1위 국가는 빨간색**으로 표시돼!")

    # MBTI 유형 선택 (Country 컬럼 제외한 나머지 컬럼들)
    mbti_types = df.columns.drop('Country').tolist()
    selected_mbti = st.selectbox("궁금한 MBTI 유형을 선택해줘:", mbti_types)

    # 데이터 정렬 및 상위 30개국 추출
    mbti_ranking = df[['Country', selected_mbti]].sort_values(by=selected_mbti, ascending=False).head(30)
    mbti_ranking.columns = ['Country', 'Percentage']

    # 색상 설정: 1등은 빨간색, 나머지는 파란색 그라데이션
    # 데이터 개수에 맞춰 파란색 색상 리스트 생성
    n_data = len(mbti_ranking)
    blue_colors = px.colors.sample_colorscale("Blues", [i/(n_data) for i in range(n_data)], low=0.4, high=0.9)
    blue_colors.reverse() # 높은 비율이 진한 파란색이 되도록 역순 정렬
    
    colors = ['#EF553B'] + blue_colors[1:]

    # Plotly 막대 그래프 생성
    fig = go.Figure(go.Bar(
        x=mbti_ranking['Country'],
        y=mbti_ranking['Percentage'],
        marker_color=colors,
        hovertemplate='<b>%{x}</b><br>비율: %{y:.2%}<extra></extra>'
    ))

    fig.update_layout(
        title=f"<b>{selected_mbti}</b> 비율이 높은 상위 30개국",
        xaxis_title="국가",
        yaxis_title="비율",
        yaxis_tickformat='.1%',
        template="plotly_white",
        height=600,
        xaxis={'categoryorder':'total descending'} # 비율 높은 순으로 정렬 유지
    )

    st.plotly_chart(fig, use_container_width=True)

    # 전체 순위 데이터 표
    with st.expander(f"{selected_mbti} 전체 국가 순위 보기"):
        full_ranking = df[['Country', selected_mbti]].sort_values(by=selected_mbti, ascending=False).reset_index(drop=True)
        st.dataframe(full_ranking.style.format({selected_mbti: '{:.2%}'}))

except FileNotFoundError:
    st.error("`countriesMBTI_16types.csv` 파일을 찾을 수 없어. 깃허브 레포지토리에 파일을 꼭 같이 올려줘!")
