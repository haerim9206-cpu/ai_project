import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="인천 식당 평점 검색 시스템", layout="wide")

# 데이터 로드 함수
@st.cache_data
def load_data():
    try:
        # utf-8로 읽고 에러는 무시하도록 처리
        df = pd.read_csv('food.csv', encoding='utf-8', errors='ignore')
        # 컬럼명 좌우 공백 제거
        df.columns = df.columns.str.strip()
        # 지역명 데이터가 있다면 공백 제거 및 문자열 변환
        if '지역명' in df.columns:
            df['지역명'] = df['지역명'].astype(str).str.strip()
        return df
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"데이터를 읽는 중 오류가 발생했습니다: {e}")
        return None

# 데이터 불러오기
df = load_data()

if df is None:
    st.error("📂 'food.csv' 파일을 찾을 수 없거나 불러오지 못했어. GitHub 저장소에 app.py와 같은 위치에 업로드했는지 꼭 확인해줘!")
else:
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
        # 입력한 검색어가 포함된 지역 필터링
        matched_regions = df[df['지역명'].str.contains(search_query, case=False, na=False)]['지역명'].unique()
        
        if len(matched_regions) == 0:
            st.error(f"❌ '{search_query}'와(과) 일치하는 지역명을 찾을 수 없어. 다시 입력해줘!")
        else:
            # 매칭된 첫 번째 지역을 기준으로 분석 진행
            selected_region = matched_regions[0]
            
            if len(matched_regions) > 1:
                st.info(f"💡 여러 지역이 검색되었어. 가장 유사한 **{selected_region}** 기준으로 결과를 보여줄게! (검색된 다른 지역: {', '.join(matched_regions[1:])})")
            
            # 선택된 지역 데이터 필터링
            region_df = df[df['지역명'] == selected_region]
            
            # '네이버평점' 컬럼 숫자로 변환 (에러 방지)
            region_df['네이버평점'] = pd.to_numeric(region_df['네이버평점'], errors='coerce')
            rated_region_df = region_df.dropna(subset=['네이버평점'])
            
            # 2. 식당 수와 평균 평점 출력
            st.header(f"📊 {selected_region} 분석 결과")
            
            total_restaurants = len(region_df)
            rated_restaurants = len(rated_region_df)
            avg_rating = rated_region_df['네이버평점'].mean() if rated_restaurants > 0 else 0
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="전체 식당 수", value=f"{total_restaurants:,} 개")
            with col2:
                st.metric(label="평균 네이버 평점", value=f"{avg_rating:.2f} / 5.0")
                
            st.markdown("---")
            
            # 3. 검색한 지역 중에서 가장 평균 평점이 높은 식당 TOP 5
            st.header(f"🏆 {selected_region} 평점 높은 식당 TOP 5")
            
            if rated_restaurants > 0:
                # 평점 기준 내림차순 정렬 후 상위 5개 추출
                top5 = rated_region_df.sort_values(by='네이버평점', ascending=False).head(5)
                
                # 지점명 결측치 처리
                if '지점명' in top5.columns:
                    top5['지점명'] = top5['지점명'].fillna('-')
                else:
                    top5['지점명'] = '-'
                    
                # 인덱스를 1부터 시작하도록 재설정
                top5_display = top5[['식당명', '지점명', '네이버평점']].reset_index(drop=True)
                top5_display.index = top5_display.index + 1
                
                # 결과 테이블 출력
                st.table(top5_display)
            else:
                st.warning("선택한 지역에 평점이 등록된 식당이 없습니다.")
    else:
        st.info("💡 위의 입력창에 검색하고 싶은 지역명(예: 연수구)을 입력하면 상세 분석 결과가 나타나!")
