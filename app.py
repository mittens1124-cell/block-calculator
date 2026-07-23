import streamlit as st
import pandas as pd
import datetime
import holidays

# 1. 페이지 설정
st.set_page_config(
    page_title="베트남 노선 그룹 블록 vs INDV 의사결정 시뮬레이터",
    page_icon="✈️",
    layout="wide"
)

# 2. 커스텀 스타일 적용 (CSS - 네이버 항공권 버튼 스타일 추가)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .status-badge-indiv {
        background-color: #e7f5ff; color: #1c7ed6;
        padding: 10px 18px; border-radius: 20px; font-weight: bold; font-size: 16px;
    }
    .status-badge-group {
        background-color: #ebfbee; color: #2b8a3e;
        padding: 10px 18px; border-radius: 20px; font-weight: bold; font-size: 16px;
    }
    .naver-btn {
        display: inline-block;
        width: 100%;
        background-color: #03C75A;
        color: white !important;
        text-align: center;
        padding: 12px 20px;
        font-size: 15px;
        font-weight: bold;
        border-radius: 8px;
        text-decoration: none;
        margin-top: 10px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .naver-btn:hover {
        background-color: #02b350;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("✈️ 베트남 노선 그룹 블록 vs INDV 손익 판단 시뮬레이터")
st.caption("노선별 건기/우기, 양국 공휴일, 요일 특성을 통합 분석하여 최적의 의사결정과 AI 전략 리포트를 제공합니다.")

st.divider()

# 3. 입력 창(좌측)과 결과 창(우측) 2컬럼 레이아웃
col_input, col_result = st.columns([1, 1.2], gap="large")

with col_input:
    st.subheader("📌 조건 입력")
    
    # 1️⃣ 노선 선택
    with st.expander("1️⃣ 노선 선택 (목적지)", expanded=True):
        route = st.selectbox(
            "목적지 노선 선택",
            options=["PQC (푸꾸옥)", "CXR (나트랑)", "DAD (다낭)", "HAN (하노이)", "HPH (하이퐁)", "SAI (사이공/호치민)"]
        )
        route_code = route.split()[0]

    # 2️⃣ 출발/운항 날짜 설정
    with st.expander("2️⃣ 출발/운항 날짜 설정 (기후 / 요일 / 공휴일)", expanded=True):
        flight_date = st.date_input("출발/운항 날짜", datetime.date.today())
        month = flight_date.month
        
        # 요일 판단
        weekday_num = flight_date.weekday()
        weekday_kr = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"][weekday_num]
        is_weekend = weekday_num in [4, 5, 6]
        
        # 🇰🇷 한국 & 🇻🇳 베트남 공휴일
        kr_holidays = holidays.KR(years=flight_date.year)
        vn_holidays = holidays.VN(years=flight_date.year)
        
        is_kr_holiday = flight_date in kr_holidays
        kr_holiday_name = kr_holidays.get(flight_date) if is_kr_holiday else ""
        
        is_vn_holiday = flight_date in vn_holidays
        vn_holiday_name = vn_holidays.get(flight_date) if is_vn_holiday else ""

        # ☀️🌧️ 노선별 건기/우기 판단 로직
        is_dry_season = False
        season_name = ""
        season_desc = ""

        if route_code == "PQC":
            is_dry_season = month in [11, 12, 1, 2, 3, 4]
            season_name = "건기 (최고 성수기)" if is_dry_season else "우기 (비수기)"
            season_desc = "휴양지 특성상 건기 시즌 모객 집중도가 매우 높은 노선입니다." if is_dry_season else "우기 시즌으로 강수량이 많아 모객 속도가 더딜 수 있습니다."
            
        elif route_code == "CXR":
            is_dry_season = month in [1, 2, 3, 4, 5, 6, 7, 8]
            season_name = "건기 (성수기)" if is_dry_season else "우기 (우천/태풍 주의)"
            season_desc = "날씨가 좋아 가족/휴양 객단가가 안정적으로 형성되는 시즌입니다." if is_dry_season else "Late Rainy Season으로 단기 우천에 따른 모객 변동성이 있습니다."
            
        elif route_code == "DAD":
            is_dry_season = month in [2, 3, 4, 5, 6, 7, 8]
            season_name = "건기 (성수기)" if is_dry_season else "우기 (태풍/우천 시즌)"
            season_desc = "스테디셀러 노선으로 건기 시즌 패키지/FIT 수요가 높습니다." if is_dry_season else "우기 및 태풍 영향을 받을 수 있어 잔여석 처리에 유의해야 합니다."
            
        elif route_code in ["HAN", "HPH"]:
            is_dry_season = month in [11, 12, 1, 2, 3]
            season_name = "건기/가을·겨울 (성수기)" if is_dry_season else "우기/고온다습 (비수기)"
            season_desc = "여행하기에 선선하고 쾌적하여 관광 상용 수요가 상승합니다." if is_dry_season else "무더위와 우기로 인해 상용 수요 중심 운항이 예상됩니다."
            
        elif route_code == "SAI":
            is_dry_season = month in [12, 1, 2, 3, 4]
            season_name = "건기 (성수기)" if is_dry_season else "우기 (스콜성 우천)"
            season_desc = "비즈니스 및 골프/관광 수요가 안정적으로 유지되는 시즌입니다." if is_dry_season else "스콜성 우천이 자주 발생하나 상용 수요는 비교적 꾸준합니다."

    # 3️⃣ 실모객 및 판매가 설정
    with st.expander("3️⃣ 실모객 및 판매가 설정", expanded=True):
        pax = st.number_input("실모객 인원 (PAX)", min_value=1, max_value=100, value=3, step=1)
        selling_price = st.number_input("1인당 판매가 (KRW)", min_value=0, value=620000, step=10000, format="%d")
        
    # 4️⃣ INDV 발권 조건
    with st.expander("4️⃣ INDV 발권 조건", expanded=True):
        indiv_net = st.number_input("INDV 1인당 NET FARE (KRW)", min_value=0, value=1069000, step=10000, format="%d")
        
    # 5️⃣ DEPO 그룹 조건
    with st.expander("5️⃣ DEPO 그룹 조건", expanded=True):
        group_net = st.number_input("그룹 1인당 NET FARE (KRW)", min_value=0.0, value=587457.1, step=1000.0, format="%.2f")
        depo_seats = st.number_input("DEPO 유지/보장 좌석 수", min_value=1, max_value=100, value=11, step=1)

    st.info("💡 **Tip:** 노선 및 날짜를 변경하면 기후 특성을 반영한 AI 전략이 즉시 업그레이드됩니다.")

# 4. 손익 계산 로직
indiv_revenue = pax * selling_price
indiv_cost = pax * indiv_net
indiv_profit = indiv_revenue - indiv_cost

group_revenue = pax * selling_price
group_cost = depo_seats * group_net
group_profit = group_revenue - group_cost

bep_pax = (depo_seats * group_net) / indiv_net if indiv_net > 0 else 0

# 5. 우측 결과 표시
with col_result:
    st.subheader(f"📊 [{route_code}] 손익 비교 및 분석 결과")
    
    # 추천 의사결정 배지
    if indiv_profit > group_profit:
        recommendation = "INDV 발권 전환"
        saved_amount = indiv_profit - group_profit
        status_html = '<div class="status-badge-indiv">💡 AI 추천: INDV 발권 전환</div>'
    else:
        recommendation = "DEPO 유지 (그룹 진행)"
        saved_amount = group_profit - indiv_profit
        status_html = '<div class="status-badge-group">💡 AI 추천: DEPO 유지 (그룹 진행)</div>'

    st.markdown(status_html, unsafe_allow_html=True)
    st.write("")

    res_c1, res_c2 = st.columns(2)
    with res_c1:
        st.metric("INDV 발권 시 손익", f"{indiv_profit:,.0f} 원", delta=f"원가 {indiv_cost:,.0f}원", delta_color="off")
    with res_c2:
        st.metric("DEPO 그룹 유지 손익", f"{group_profit:,.0f} 원", delta=f"원가 {group_cost:,.0f}원", delta_color="off")

    st.success(f"**최종 판단:** {recommendation} (상대 선택 대비 **약 {saved_amount:,.0f}원** 손실 절감 가능)")

    df_summary = pd.DataFrame({
        "구분": ["INDV 발권", "DEPO 그룹 유지"],
        "적용 좌석": [f"{pax}석", f"{depo_seats}석"],
        "총 매출": [f"{indiv_revenue:,.0f}원", f"{group_revenue:,.0f}원"],
        "총 원가": [f"{indiv_cost:,.0f}원", f"{group_cost:,.0f}원"],
        "최종 손익": [f"{indiv_profit:,.0f}원", f"{group_profit:,.0f}원"]
    })
    st.dataframe(df_summary, use_container_width=True, hide_index=True)

    # 6. 노선 기후 & 양국 공휴일 요약 박스
    st.markdown("---")
    st.subheader(f"🗺️ [{route_code} 노선] 기후 및 달력 특성")
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.write(f"🏖️ **노선 기후**: **{season_name}** ({flight_date.month}월)")
        st.caption(f"• {season_desc}")
        
    with col_d2:
        st.write(f"📆 **운항일**: **{flight_date.strftime('%Y-%m-%d')} ({weekday_kr})**")
        holiday_tags = []
        if is_kr_holiday: holiday_tags.append(f"🇰🇷 {kr_holiday_name}")
        if is_vn_holiday: holiday_tags.append(f"🇻🇳 {vn_holiday_name}")
        
        if holiday_tags:
            st.warning(f"🎉 **공휴일 태그**: {', '.join(holiday_tags)}")
        elif is_weekend:
            st.info(f"🔥 **주말 패턴**: {weekday_kr} 운항 (주말 출국 선호)")
        else:
            st.caption("💼 일반 주중 평일 패턴")

    # --------------------------------------------------------------------------
    # 🔗 네이버 실시간 동적 URL 생성 및 버튼 표시 (AI 리포트 바로 위)
    # --------------------------------------------------------------------------
 st.markdown("---")
    
    # YYYYMMDD 포맷 (예: 20260807)
    date_str_compact = flight_date.strftime("%Y%m%d")
    
    # 🟢 네이버 항공권 정확한 검색 URL (입력한 날짜/노선 자동 세팅)
    naver_url = f"https://flight.naver.com/flights/oneWay/SEL-{route_code}-{date_str_compact}?adult=1&isDirect=true&fareType=Y"
    
    # 네이버 항공권 단독 큰 버튼 출력
    st.markdown(
        f'<a href="{naver_url}" target="_blank" class="naver-btn">🟢 네이버 항공권 실시간 조회 ({route_code} {flight_date}) ↗</a>',
        unsafe_allow_html=True
    )
    # 7. AI 종합 전략 리포트
    st.subheader("🤖 AI 종합 전략 리포트 (Comment)")
    
    # 노선 기후 기반 코멘트
    climate_comment = f"• **[{route_code} {season_name}]** {season_desc}"
    if is_dry_season:
        climate_comment += " (건기 특수로 D-10 시점까지 추가 모객 가능성이 높습니다.)"
    else:
        climate_comment += " (우기 시즌이므로 모객 속도가 느릴 수 있으니 무리한 그룹 유지보다는 보수적 대응이 유리합니다.)"

    # 날짜 공휴일 코멘트
    date_comment = []
    if is_kr_holiday:
        date_comment.append(f"• **[한국 연휴 특수]** 한국 {kr_holiday_name} 연휴로 출국 수요 폭증 구간입니다.")
    elif is_weekend:
        date_comment.append(f"• **[주말 패턴]** {weekday_kr} 출발 건으로 주말 선호 모객 우수가 예상됩니다.")
    
    if is_vn_holiday:
        date_comment.append(f"• **[베트남 현지 연휴]** 현지 {vn_holiday_name} 기간으로 현지 지상비 및 인바운드 상황을 체크하세요.")

    date_comment_str = "\n".join(date_comment) if date_comment else "• **[일반 날짜]** 특이 공휴일 없는 평일 노선입니다."

    if indiv_profit > group_profit:
        comment_text = f"""
**[AI 분석 의견: INDV 전환 강력 권장]**

• **손익분기점 분석:** 현재 실모객({pax}명)은 손익분기점({bep_pax:.1f}명) 미달 상태입니다.
• **위험 요인:** DEPO 납입 후 그룹을 유지할 경우 발생할 손실(-{abs(group_profit):,.0f}원)이 너무 큽니다.
• **비용 절감 효과:** INDV로 전환 발권 시, 그룹 유지 대비 **약 {saved_amount:,.0f}원**의 손실을 방지(절감)할 수 있습니다.
• 💡 **액션 플랜:** 그룹 블록을 즉시 취소/해제하고 개별 발권을 진행하십시오.

---
**🌤️ 노선 기후 & 🗓️ 공휴일 반영 추가 전략:**
{climate_comment}
{date_comment_str}
        """
        st.warning(comment_text)
    else:
        comment_text = f"""
**[AI 분석 의견: DEPO 유지 및 그룹 진행 권장]**

• **손익분기점 분석:** 현재 실모객({pax}명)이 손익분기점({bep_pax:.1f}명) 이상이거나, INDV 운임이 매우 비쌉니다.
• **위험 요인:** {depo_seats}석 전체 운임(-{group_cost:,.0f}원)을 부담하더라도 그룹을 끌고 가는 것이 손실을 줄이는 길입니다.
• **비용 절감 효과:** INDV 전환 대비 **약 {saved_amount:,.0f}원**의 비용을 절감할 수 있습니다.
• 💡 **액션 플랜:** DEPO를 납입하여 블록을 유지하고, 남은 D-10(풀페이) 시점까지 추가 모객에 집중하십시오.

---
**🌤️ 노선 기후 & 🗓️ 공휴일 반영 추가 전략:**
{climate_comment}
{date_comment_str}
        """
        st.success(comment_text)
