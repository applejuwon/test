import streamlit as st
import folium
from streamlit_folium import st_folium

# -----------------------------
# 1. 앱 기본 설정
# -----------------------------
st.set_page_config(page_title="Sea Level Simulator", layout="wide")
st.title("Sea Level Simulator - Global Flood Simulation")

# -----------------------------
# 2. 해수면 상승 슬라이더
# -----------------------------
sea_level = st.slider("Sea level rise (m)", 0, 50, 5)

# -----------------------------
# 3. 도시 좌표 미리 정의
# -----------------------------
city_coords = {
    "Seoul": (37.5665, 126.9780),
    "New York": (40.7128, -74.0060),
    "London": (51.5074, -0.1278),
    "Tokyo": (35.6895, 139.6917),
    "Sydney": (-33.8688, 151.2093),
    "Paris": (48.8566, 2.3522),
    "Cairo": (30.0444, 31.2357),
    "Rio de Janeiro": (-22.9068, -43.1729)
}

selected_cities = st.multiselect(
    "Select cities to display",
    options=list(city_coords.keys()),
    default=["Seoul", "New York"]
)

# -----------------------------
# 4. 지도 생성 (전 세계)
# -----------------------------
m = folium.Map(location=[0, 0], zoom_start=2)

# -----------------------------
# 5. 도시 위치 + 침수 원 표시
# -----------------------------
for city in selected_cities:
    lat, lon = city_coords[city]
    # 단순 예시: 해수면 25m 이상이면 침수
    flooded = sea_level >= 25
    color_marker = "red" if flooded else "green"
    popup_text = f"{city} - Flood: {'Yes' if flooded else 'No'}"
    
    # 도시 마커
    folium.Marker(
        location=[lat, lon],
        popup=popup_text,
        icon=folium.Icon(color=color_marker)
    ).add_to(m)
    
    # 침수 원 (파란색, 투명도 조정)
    if flooded:
        folium.Circle(
            location=[lat, lon],
            radius=50000 + sea_level*1000,  # 슬라이더 값에 따라 원 크기 조절
            color="blue",
            fill=True,
            fill_opacity=0.3,
            popup=f"{city} flooded area"
        ).add_to(m)

# -----------------------------
# 6. Streamlit에서 지도 표시
# -----------------------------
st_data = st_folium(m, width=1200, height=650)
