import os
import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    # 현재 파일(06_수행평가.py)의 절대 경로 기준 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "..", "food.csv")

    # 인코딩 오류 해결을 위한 에러 핸들링 구조
    try:
        # 1. 먼저 한글 깨짐이 가장 자주 발생하는 cp949 인코딩으로 시도
        df = pd.read_csv(csv_path, encoding="cp949")
    except UnicodeDecodeError:
        try:
            # 2. 실패 시 utf-8 인코딩으로 시도
            df = pd.read_csv(csv_path, encoding="utf-8")
        except UnicodeDecodeError:
            # 3. 그것도 실패 시 BOM이 포함된 utf-8-sig로 최종 시도
            df = pd.read_csv(csv_path, encoding="utf-8-sig")

    # 컬럼명 공백 제거 및 평점 숫자형 변환
    df.columns = df.columns.str.strip()
    df["네이버평점"] = pd.to_numeric(df["네이버평점"], errors="coerce")

    # 지점명과 식당명의 결측치를 빈 문자열로 대체 (텍스트 검색용)
    df["지점명"] = df["지점명"].fillna("").astype(str)
    df["식당명"] = df["식당명"].fillna("").astype(str)

    return df


df = load_data()

st.title("🍴 지역별 식당 평점 분석 대시보드")
st.markdown("---")

# 2. 지역 선택 (데이터 특징에 맞게 조회하고 싶은 주요 지역 키워드 구성)
region_keywords = [
    "전체",
    "송도",
    "월미도",
    "부평",
    "구월",
    "주안",
    "고잔",
    "남촌",
]
selected_region = st.selectbox("분석할 지역(키워드)을 선택해줘:", region_keywords)

# 3. 선택한 지역에 맞게 데이터 필터링
if selected_region == "전체":
    filtered_df = df.copy()
else:
    # 식당명이나 지점명에 해당 지역 키워드가 포함된 데이터만 필터링
    filtered_df = df[
        df["식당명"].str.contains(selected_region)
        | df["지점명"].str.contains(selected_region)
    ]

# 평점이 존재하는 데이터만 따로 분리 (통계 및 TOP 5 계산용)
rated_df = filtered_df.dropna(subset=["네이버평점"])

# --- 요구사항 2: 식당 수와 평균 평점 표시 ---
st.subheader(f"📍 {selected_region} 지역 요약 정보")

col1, col2 = st.columns(2)

with col1:
    total_count = len(filtered_df)
    st.metric(label="총 식당 수 (구내식당 포함)", value=f"{total_count:,}개")

with col2:
    if not rated_df.empty:
        avg_rating = rated_df["네이버평점"].mean()
        st.metric(label="평균 네이버 평점", value=f"{avg_rating:.2f} / 5.0")
    else:
        st.metric(label="평균 네이버 평점", value="데이터 없음")

st.markdown("---")

# --- 요구사항 3: 평균 평점이 높은 식당 Top 5 ---
st.subheader(f"⭐ {selected_region} 지역 평점 높은 식당 TOP 5")

if not rated_df.empty:
    # 평점 기준 내림차순 정렬 후 상위 5개 추출
    top5 = (
        rated_df.sort_values(by="네이버평점", ascending=False)
        .head(5)[["식당명", "지점명", "네이버평점"]]
        .reset_index(drop=True)
    )

    # 인덱스를 1부터 시작하도록 변경
    top5.index = top5.index + 1

    # 테이블 형태로 깔끔하게 출력
    st.table(top5)
else:
    st.warning("이 지역에는 평점 데이터가 등록된 식당이 없어!")

# 필터링된 전체 데이터 확인용 확장 탭
with st.expander("선택한 지역의 전체 데이터 보기"):
    st.dataframe(filtered_df)
