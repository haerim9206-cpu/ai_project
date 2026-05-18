import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="서울 외국인 인기 관광지 Top 10", layout="wide")

st.title("🗺️ 외국인이 좋아하는 서울 관광지 Top 10")
st.markdown("지도의 마커를 클릭하면 하단에서 **가까운 지하철역**과 **추천 놀거리**를 볼 수 있어!")

# 관광지 데이터
spots = [
    {"name": "경복궁", "lat": 37.5796, "lng": 126.9770, "station": "3호선 경복궁역", "fun": "한복 대여 체험 및 광화문 광장 산책"},
    {"name": "N서울타워 (남산)", "lat": 37.5512, "lng": 126.9882, "station": "4호선 명동역 (케이블카 이용)", "fun": "서울 시내 전망 감상 및 사랑의 자물쇠 걸기"},
    {"name": "명동거리", "lat": 37.5629, "lng": 126.9850, "station": "4호선 명동역 / 2호선 을지로입구역", "fun": "길거리 음식 탐방 및 K-뷰티 쇼핑"},
    {"name": "인사동 쌈지길", "lat": 37.5744, "lng": 126.9848, "station": "3호선 안국역", "fun": "전통 찻집 방문 및 한국 전통 공예품 구경"},
    {"name": "동대문디자인플라자 (DDP)", "lat": 37.5665, "lng": 127.0092, "station": "2/4/5호선 동대문역사문화공원역", "fun": "독특한 건축물 전시 관람 및 패션 마켓 쇼핑"},
    {"name": "롯데월드 & 서울스카이", "lat": 37.5111, "lng": 127.0982, "station": "2/8호선 잠실역", "fun": "스릴 넘치는 놀이기구 탑승 및 초고층 전망대 야경 감상"},
    {"name": "북촌한옥마을", "lat": 37.5829, "lng": 126.9835, "station": "3호선 안국역", "fun": "실제 한옥 주거지 골목길에서 인생샷 남기기"},
    {"name": "홍대 걷고싶은거리", "lat": 37.5567, "lng": 126.9234, "station": "2호선/공항철도 홍대입구역", "fun": "버스킹 공연 관람, 이색 카페 및 클럽 문화 체험"},
    {"name": "국립중앙박물관", "lat": 37.5238, "lng": 126.9804, "station": "4호선/경의중앙선 이촌역", "fun": "한국의 역사 유물 관람 및 야외 거울못 정원 산책"},
    {"name": "강남역 & 별마당도서관", "lat": 37.5119, "lng": 127.0589, "station": "2호선 삼성역 (코엑스몰 연결)", "fun": "거대한 오픈 도서관 포토존 인증샷 및 코엑스몰 쇼핑"}
]

# 지도 생성
m = folium.Map(location=[37.555, 126.992], zoom_start=12)

for spot in spots:
    folium.Marker(
        location=[spot["lat"], spot["lng"]],
        popup=spot["name"],
        tooltip=spot["name"]
    ).add_to(m)

# st_folium 지도 렌더링
map_data = st_folium(m, width=1000, height=500, key="seoul_tour_map_v3")

st.markdown("---")
st.subheader("🔍 선택한 관광지 상세 정보")

selected_spot = None

# 마커 클릭 이벤트 안전하게 수신
if map_data and map_data.get("last_object_clicked"):
    click_info = map_data["last_object_clicked"]
    click_lat = click_info.get("lat")
    click_lng = click_info.get("lng")
    
    if click_lat and click_lng:
        for spot in spots:
            if abs(spot["lat"] - click_lat) < 0.005 and abs(spot["lng"] - click_lng) < 0.005:
                selected_spot = spot
                break

if selected_spot:
    st.success(f"📍 **{selected_spot['name']}**")
    st.info(f"🚇 **가까운 지하철역:** {selected_spot['station']} | 🎡 **추천 놀거리:** {selected_spot['fun']}")
else:
    st.write("지도의 마커를 클릭하면 상세 정보가 한 줄 요약되어 여기에 표시돼.")
