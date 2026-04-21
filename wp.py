import streamlit as st
import math
import pandas as pd
from streamlit_folium import st_folium
import folium

# --- [하드코딩 데이터] ---
CAFE_DATA = [
    {"이름": "Lucky Archive 428", "주소": "오디너리 아카이브", "lat": 37.5571717, "lon": 126.9293252, "오픈": "12:00", "기본특전": "종이컵+엽서+2종+투명포카+스티커+트레카+스티커+스탬프판+부채", "럭드": "O", "포토부스": "O", "특이사항":"코지클라우드님!", "공지":"https://x.com/1uckyarchive/status/2040330550133879097"},
    {"이름": "삼십삼돌", "주소": "미닝 더 갤러리", "lat": 37.5551888, "lon": 126.9269387, "오픈": "12:00", "기본특전": "스티커+네컷사진+엽서+트레카2장", "럭드": "O", "포토부스": "X", "특이사항":"-", "공지":"https://x.com/wp_april28/status/2033196554283270636"},
    {"이름": "Toward - 4:28", "주소": "다이버시티", "lat": 37.5554637, "lon": 126.9245478, "오픈": "11:00", "기본특전": "종이컵+엽서+투명포카+스티커", "럭드": "O", "포토부스": "O", "특이사항":"-", "공지":"https://x.com/toward428/status/2030908514823274980"},
    {"이름": "Peace of Heaven", "주소": "히치하이킹클럽", "lat": 37.5487553, "lon": 126.9193894, "오픈": "-", "기본특전": "종이컵+포스터+보틀스티커+트레카2장", "럭드": "O", "포토부스": "O", "특이사항":"에센셜님", "공지":"https://x.com/__ESSENTIAL/status/2031196457886453936"},
    {"이름": "행운의 증명", "주소": "카페 플래닛", "lat": 37.5551902, "lon": 126.9271981, "오픈": "11:00", "기본특전": "종이컵+연력+아크릴키링", "럭드": "O", "포토부스": "X", "특이사항":"MISTY님", "공지":"https://x.com/themisty__/status/2031633282048393524"},
    {"이름": "1000개의 별을 접어서", "주소": "몰리스피크닉", "lat": 37.5559906, "lon": 126.9260605, "오픈": "12:00", "기본특전": "종이컵+엽서+스티커팩+별종이", "럭드": "O", "포토부스": "O", "특이사항":"-", "공지":"https://x.com/myhappilness/status/2032080338890211589"},
    {"이름": "이삭피아노", "주소": "하트클립", "lat": 37.5554056, "lon": 126.9303515, "오픈": "13:00", "기본특전": "종이컵+엽서+티코스터", "럭드": "O", "포토부스": "O", "특이사항":"떡꼬치", "공지":"https://x.com/_pponyoo__/status/2032411979198116030"},
    {"이름": "428번째 플레이리스트", "주소": "도레미", "lat": 37.5554988, "lon": 126.9264304, "오픈": "12:00", "기본특전": "종이컵+엽서+포카+스티커", "럭드": "O", "포토부스": "X", "특이사항":"-", "공지":"https://x.com/428pilay/status/2033506109315805369"},
    {"이름": "PIL so good", "주소": "하이럽", "lat": 37.5496255, "lon": 126.9197412, "오픈": "12:00", "기본특전": "종이컵+티켓+포카+스티커", "럭드": "O", "포토부스": "X", "특이사항":"-", "공지":"https://x.com/DAYDAYHBD/status/2035620858887381250"},
    {"이름": "Pilower Garden", "주소": "비데이 홍대점", "lat": 37.5549328, "lon": 126.9267345, "오픈": "-", "기본특전": "종이컵+엽서+보틀스티커+핀뱃지+포카2장", "럭드": "O", "포토부스": "X", "특이사항":"얼리버드", "공지":"https://x.com/day6_bdays/status/2036327234999664909"},
    {"이름": "토끼지만 용맹합니다", "주소": "카페 헤이", "lat": 37.5556389, "lon": 126.9266043, "오픈": "11:00", "기본특전": "종이컵+스트로우토퍼+부채+스티커팩+물티슈", "럭드": "O", "포토부스": "X", "특이사항":"-", "공지":"https://x.com/BraveBunny_Pil/status/2038492171356323996"},
    {"이름": "Happiily ever after", "주소": "쿠잉 스테이션", "lat": 37.5554988, "lon": 126.9264304, "오픈": "11:00", "기본특전": "종이컵+엽서팩+연력+DIY초대장", "럭드": "O", "포토부스": "O", "특이사항":"-", "공지":"https://x.com/dearmyfirstluv_/status/2039606003273199689"},
    {"이름": "원필이의 행운 나눔소", "주소": "아이니드케이크", "lat": 37.5566766, "lon": 126.9293946, "오픈": "12:00", "기본특전": "종이컵+엽서 2종+스티커", "럭드": "O (갓챠)", "포토부스": "X", "특이사항":"-", "공지":"https://x.com/hbd904904/status/2040310279859495211"},
    {"이름": "필이네 행운판매소", "주소": "신드롬", "lat": 37.5548785, "lon": 126.9287544, "오픈": "12:00", "기본특전": "종이컵+엽서+포카+스티커+행운카드+행운클로버키링", "럭드": "O", "포토부스": "X", "특이사항":"-", "공지":"https://x.com/101_HBD/status/2041866943553241312"},
]

def get_walking_time(p1, p2):
    distance_deg = math.sqrt((p1['lat'] - p2['lat'])**2 + (p1['lon'] - p2['lon'])**2)
    distance_km = distance_deg * 111
    return max(1, int(distance_km * 15))

def optimize_route(selected_cafes):
    if len(selected_cafes) <= 2: return selected_cafes
    path = selected_cafes[:2]
    unvisited = selected_cafes[2:]
    while unvisited:
        next_node = min(unvisited, key=lambda x: get_walking_time(path[-1], x))
        path.append(next_node)
        unvisited.remove(next_node)
    return path

st.set_page_config(page_title="원필이 생카 계획짜기", layout="centered")
st.title("🍀🐰 0428 원필이 생카!! 🐰🍀")
st.divider()


st.subheader("카페를 선택하세용~")
# 동적 선택 리스트 구성을 위한 변수
temp_selected = [CAFE_DATA[0], CAFE_DATA[1]]
cols = st.columns(2)

for i in range(0, len(CAFE_DATA), 2):
    row_cafes = CAFE_DATA[i:i+2]
    cols = st.columns(2)
    
    for j, cafe in enumerate(row_cafes):
        idx = i + j
        with cols[j]:
            # 0, 1번은 기본 체크
            default_val = True if idx < 2 else False
            is_checked = st.checkbox(f"{cafe['이름']}", key=f"check_{idx}", value=default_val)
            
            if is_checked:
                temp_selected.append(cafe)
            
            # 요청하신 형식을 그대로 유지한 토글 부분
            with st.expander(f"🏠 {cafe['주소']}"):
                st.write(f"🕒 **오픈:** {cafe['오픈']}")
                st.write(f"🎁 **특전:** {cafe['기본특전']}")
                st.write(f"🍀 **럭드:** {cafe['럭드']}  📸 **부스:** {cafe['포토부스']}")
                if cafe["특이사항"] != "-":
                    st.write(f"💡 **특이사항:** {cafe['특이사항']}")

                st.markdown(f"🔗 [트위터 공지]({cafe['공지']})")

# 2. 동선 업데이트 및 최적화
st.divider()
button_con = st.container()

with button_con:
    if st.button("📝 투어 리스트 생성", use_container_width=True, type="primary"):
        st.session_state.route = temp_selected
    
# 3. 결과 출력
if 'route' in st.session_state and st.session_state.route:
    total_time = 0
    st.divider()
    st.subheader("📍 경로")
    
    for i, cafe in enumerate(st.session_state.route):
        with st.expander(f"**{i+1}. {cafe['이름']}**", expanded=True):
            st.write(f"🏠 **위치:** {cafe['주소']}")
            st.write(f"🎁 **특전:** {cafe['기본특전']}")
            st.write(f"🕒 **오픈:** {cafe['오픈']}  🍀 **럭드:** {cafe['럭드']}  📸 **부스:** {cafe['포토부스']}")
            # 상세 리스트에서도 링크 클릭 방식으로 수정
            st.markdown(f"🔗 [공지]({cafe['공지']})")
            
            c1, c2, c3 = st.columns([1, 1, 2])
            if c1.button("▲", key=f"up_{i}"):
                if i > 0:
                    st.session_state.route[i], st.session_state.route[i-1] = st.session_state.route[i-1], st.session_state.route[i]
                    st.rerun()
            if c2.button("▼", key=f"down_{i}"):
                if i < len(st.session_state.route)-1:
                    st.session_state.route[i], st.session_state.route[i+1] = st.session_state.route[i+1], st.session_state.route[i]
                    st.rerun()
            with c3:
                st.link_button("네이버 지도", f"https://map.naver.com/v5/search/{cafe['주소']}", use_container_width=True)

        if i < len(st.session_state.route) - 1:
            t = get_walking_time(cafe, st.session_state.route[i+1])
            total_time += t
            st.markdown(f"<p style='text-align:center; color:gray; font-size: 0.8rem;'>🚶‍♂️ 다음 장소까지 약 {t}분</p>", unsafe_allow_html=True)

    st.success(f"🚩 총 {len(st.session_state.route)}곳 방문 | 🚶‍♂️ 총 예상 도보 {total_time}분 (직선거리 기준, 정확한 시간은 네이버 지도로 보세용)")

    # 지도 표시
    st.subheader("🗺️ 투어 경로 지도")
    avg_lat = sum(c['lat'] for c in st.session_state.route) / len(st.session_state.route)
    avg_lon = sum(c['lon'] for c in st.session_state.route) / len(st.session_state.route)
    
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=15, tiles='CartoDB positron')
    
    for i, cafe in enumerate(st.session_state.route):

        popup_html = f"""
            <div style="font-family: 'Nanum Gothic', sans-serif; font-size: 13px;">
                <b>{cafe['이름']}</b><br>
                <a href="{cafe['공지']}" target="_blank" style="color: #1DA1F2; text-decoration: none;"> 공지 바로가기 </a>
            </div>
        """
        
        folium.Marker(
            [cafe['lat'], cafe['lon']],
            tooltip=cafe['이름'],
            popup=folium.Popup(popup_html, max_width=200),
            icon=folium.Icon(color = 'pink', icon = 'music')
        ).add_to(m)
    
    st_folium(m, width=700, height=500)
