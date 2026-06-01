import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="인천 식당 평점 데이터 분석", layout="wide")

# 데이터 로드 함수 (캐싱 처리로 속도 향상)
@st.cache_data
def load_data():
    # 파일 인코딩 및 결측치 처리
    df = pd.read_csv('food.csv', encoding='cp949')
    return df

try:
    df = load_data()
    
    st.title("🍽️ 인천 지역별 식당 평점 분석 대시보드")
    st.markdown("---")
    
    # 1. 지역 선택 사이드바
    # 결측치 제거 후 고유 지역명 정렬
    regions = sorted(df['지역명'].dropna().unique())
    selected_region = st.sidebar.selectbox("📍 분석할 지역을 선택하세요", regions)
    
    # 선택된 지역 데이터 필터링
    region_df = df[df['지역명'] == selected_region]
    
    # 평점이 있는 데이터만 따로 필터링 (통계 및 TOP 5용)
    rated_region_df = region_df.dropna(subset=['네이버평점'])
    
    # 2. 지역별 주요 통계 지표
    st.header(f"📊 {selected_region} 주요 통계")
    
    total_restaurants = len(region_df)
    rated_restaurants = len(rated_region_df)
    avg_rating = rated_region_df['네이버평점'].mean() if rated_restaurants > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="전체 식당 수", value=f"{total_restaurants:,} 개")
    with col2:
        st.metric(label="평점 등록 식당 수", value=f"{rated_restaurants:,} 개")
    with col3:
        st.metric(label="평균 네이버 평점", value=f"{avg_rating:.2f} / 5.0")
        
    st.markdown("---")
    
    # 3. 가장 평균 평점이 높은 식당 TOP 5
    st.header(f"🏆 {selected_region} 평점 높은 식당 TOP 5")
    
    if rated_restaurants > 0:
        # 평점 기준 내림차순 정렬 후 상위 5개 추출
        # 필요한 컬럼만 선택하고 보기 좋게 가공
        top5 = rated_region_df.sort_values(by='네이버평점', ascending=False).head(5)
        
        # 지점명이 없는 경우 빈칸 처리
        top5['지점명'] = top5['지점명'].fillna('-')
        
        # 인덱스를 1부터 시작하도록 변경
        top5_display = top5[['식당명', '지점명', '네이버평점']].reset_index(drop=True)
        top5_display.index = top5_display.index + 1
        
        # 스트림릿 테이블로 출력
        st.table(top5_display)
    else:
        st.warning("선택한 지역에 평점이 등록된 식당이 없습니다.")

except FileNotFoundError:
    st.error("📂 'food.csv' 파일을 찾을 수 없습니다. GitHub 저장소에 앱 코드와 같은 위치에 업로드해 주세요.")
except Exception as e:
    st.error(f"❌ 오류가 발생했습니다: {e}")
