import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="인천 식당 평점 데이터 분석", layout="wide")

# 데이터 로드 함수 (utf-8 인코딩 적용)
@st.cache_data
def load_data():
    # 기본 utf-8로 읽고, 문제 발생 시 오류 무시하도록 설정
    df = pd.read_csv('food.csv', encoding='utf-8', errors='ignore')
    # 컬럼명 좌우 공백 제거
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()
    
    st.title("🍽️ 인천 지역별 식당 평점 분석 대시보드")
    st.markdown("---")
    
    # 1. 메인 화면에 지역 선택 박스 배치
    # 결측치를 제거하고 유효한 지역명만 추출해서 가나다순 정렬
    regions = sorted(df['지역명'].dropna().unique())
    
    selected_region = st.selectbox(
        "📍 분석하고 싶은 지역명을 선택해줘:", 
        options=regions,
        index=0
    )
    
    st.markdown("---")
    
    # 선택된 지역 데이터 필터링
    region_df = df[df['지역명'] == selected_region]
    
    # 평점이 있는 데이터만 따로 필터링 (평균 평점 및 TOP 5 계산용)
    rated_region_df = region_df.dropna(subset=['네이버평점'])
    
    # 2. 선택한 지역의 식당 수와 평균 평점 출력
    st.header(f"📊 {selected_region} 분석 결과")
    
    total_restaurants = len(region_df)
    rated_restaurants = len(rated_region_df)
    avg_rating = rated_region_df['네이버평점'].mean() if rated_restaurants > 0 else 0
    
    # 카드 형태로 깔끔하게 시각화
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="전체 식당 수", value=f"{total_restaurants:,} 개")
    with col2:
        st.metric(label="평균 네이버 평점", value=f"{avg_rating:.2f} / 5.0")
        
    st.markdown("---")
    
    # 3. 가장 평균 평점이 높은 식당 TOP 5
    st.header(f"🏆 {selected_region} 평점 높은 식당 TOP 5")
    
    if rated_restaurants > 0:
        # 평점 기준 내림차순 정렬 후 상위 5개 추출
        top5 = rated_region_df.sort_values(by='네이버평점', ascending=False).head(5)
        
        # 지점명이 없는 경우 빈칸 처리
        if '지점명' in top5.columns:
            top5['지점명'] = top5['지점명'].fillna('-')
        else:
            top5['지점명'] = '-'
            
        # 순위를 1부터 보이도록 인덱스 재설정
        top5_display = top5[['식당명', '지점명', '네이버평점']].reset_index(drop=True)
        top5_display.index = top5_display.index + 1
        
        # 표로 깔끔하게 출력
        st.table(top5_display)
    else:
        st.warning("선택한 지역에 평점이 등록된 식당이 없습니다.")

except FileNotFoundError:
    st.error("📂 'food.csv' 파일을 찾을 수 없어. GitHub 저장소에 app.py와 같은 위치에 업로드했는지 확인해 줘!")
except Exception as e:
    st.error(f"❌ 오류가 발생했어: {e}")
