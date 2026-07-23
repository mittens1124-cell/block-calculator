import streamlit as st
import pandas as pd
import datetime
import holidays

# 1. 페이지 설정
st.set_page_config(
    page_title="베트남 노선 DEPO 전/후 통합 손익 판단 시뮬레이터",
    page_icon="✈️",
    layout="wide"
)

# 2. 커스텀 스타일 (CSS) - 탭 음영 및 디자인
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    
    /* 📌 탭(Tab) 음영 및 하이라이트 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid #dee2e6;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        background-color: #e9ecef;
        border-radius: 8px 8px 0 0;
        padding: 10px 22px;
        font-weight: bold;
        color: #495057 !important;
        font-size: 16px;
        border: 1px solid #ced4da;
        border-bottom: none;
        transition: all 0.2s ease-in-out;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #dee2e6;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1c7ed6 !important;
        color: #ffffff !important;
        border-color: #1c7ed6 !important;
        box-shadow: 0 -2px 6px rgba(0,0,0,0.1);
    }
    
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

st.title("✈️ 베트남 노선 그룹 블록 손익 판단 시뮬레이터")
st.caption("상단 탭을 통해 DEPO 전 시뮬레이션과 DEPO 후 (GV10 미만) 손익 계산을 손쉽게 전환하여 확인하세요.")

st.divider()

# --------------------------------------------------------------------------
# 📁 시트 탭 구성
# --------------------------------------------------------------------------
tab_sheet1, tab_sheet2 = st.tabs(["📋 DEPO 전 시뮬레이터", "📦 DEPO 후 (GV10 미만) 시뮬레이터"])

# ==========================================================================
# 📋 [DEPO 전 시뮬레이터]
# ==========================================================================
with tab_sheet1:
    col_input1, col_result1 = st.columns([1, 1.2], gap="large")

    with col_input1:
        st.subheader("📌 [DEPO 전] 조건 입력")
        
        with st.expander("1️⃣ 노선 선택 (목적지)", expanded=True):
            route1 = st.selectbox(
                "목적지 노선 선택",
                options=["PQC (푸꾸옥)", "CXR (나트랑)", "DAD (다낭)", "HAN (하노이)", "HPH (하이퐁)", "SAI (사이공/호치민)"],
                key="r1"
            )
            route_code1 = route1.split()[0]

        with st.expander("2️⃣ 출발/운항 날짜 설정", expanded=True):
            flight_date1 = st.date_input("출발/운항 날짜", datetime.date.today(), key="d1")
            month1 = flight_date1.month
            
            weekday_num1 = flight_date1.weekday()
            weekday_kr1 = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"][weekday_num1]
            is_weekend1 = weekday_num1 in [4, 5, 6]
            
            kr_holidays1 = holidays.KR(years=flight_date1.year)
            vn_holidays1 = holidays.VN(years=flight_date1.year)
            
            is_kr_holiday1 = flight_date1 in kr_holidays1
            kr_holiday_name1 = kr_holidays1.get(flight_date1) if is_kr_holiday1 else ""
            
            is_vn_holiday1 = flight_date1 in vn_holidays1
            vn_holiday_name1 = vn_holidays1.get(flight_date1) if is_vn_holiday1 else ""

            # 기후 로직
            is_dry1 = False
            season_name1, season_desc1 = "", ""
            if route_code1 == "PQC":
                is_dry1 = month1 in [11, 12, 1, 2, 3, 4]
                season_name1 = "건기 (최고 성수기)" if is_dry1 else "우기 (비수기)"
                season_desc1 = "휴양지 특성상 건기 시즌 모객 집중도가 매우 높은 노선입니다." if is_dry1 else "우기 시즌으로 강수량이 많아 모객 속도가 더딜 수 있습니다."
            elif route_code1 == "CXR":
                is_dry1 = month1 in [1, 2, 3, 4, 5, 6, 7, 8]
                season_name1 = "건기 (성수기)" if is_dry1 else "우기 (우천/태풍 주의)"
                season_desc1 = "가족/휴양 객단가가 안정적으로 형성되는 시즌입니다." if is_dry1 else "Late Rainy Season으로 우천 변동성이 있습니다."
            else:
                is_dry1 = month1 in [1, 2, 3, 4, 11, 12]
                season_name1 = "건기 시즌" if is_dry1 else "우기 시즌"
                season_desc1 = "정규 건기/우기 스케줄에 맞춰 대응하세요."

        with st.expander("3️⃣ 실모객 및 판매가 설정", expanded=True):
            pax1 = st.number_input("실모객 인원 (PAX)", min_value=1, max_value=100, value=3, step=1, key="pax1")
            selling_price1 = st.number_input("1인당 판매가 (KRW)", min_value=0, value=620000, step=10000, key="sp1")
            
        with st.expander("4️⃣ INDV 발권 조건", expanded=True):
            indiv_net1 = st.number_input("INDV 1인당 NET FARE (KRW)", min_value=0, value=1069000, step=10000, key="inet1")
            
        with st.expander("5️⃣ DEPO 그룹 조건", expanded=True):
            group_net1 = st.number_input("그룹 1인당 NET FARE (KRW)", min_value=0.0, value=587457.1, step=1000.0, key="gnet1")
            depo_seats1 = st.number_input("DEPO 유지/보장 좌석 수", min_value=1, max_value=100, value=11, step=1, key="gseats1")

    # 계산
    indiv_rev1 = pax1 * selling_price1
    indiv_cost1 = pax1 * indiv_net1
    indiv_prof1 = indiv_rev1 - indiv_cost1

    group_rev1 = pax1 * selling_price1
    group_cost1 = depo_seats1 * group_net1
    group_prof1 = group_rev1 - group_cost1
    
    bep_pax1 = group_cost1 / selling_price1 if selling_price1 > 0 else 0

    with col_result1:
        st.subheader(f"📊 [{route_code1}] DEPO 전 손익 비교")
        
        if indiv_prof1 > group_prof1:
            rec1 = "INDV 발권 전환"
            saved1 = indiv_prof1 - group_prof1
            st.markdown('<div class="status-badge-indiv">💡 AI 추천: INDV 발권 전환</div>', unsafe_allow_html=True)
        else:
            rec1 = "DEPO 유지 (그룹 진행)"
            saved1 = group_prof1 - indiv_prof1
            st.markdown('<div class="status-badge-group">💡 AI 추천: DEPO 유지 (그룹 진행)</div>', unsafe_allow_html=True)

        st.write("")
        c1, c2 = st.columns(2)
        c1.metric("INDV 발권 시 손익", f"{indiv_prof1:,.0f} 원", delta=f"원가 {indiv_cost1:,.0f}원", delta_color="off")
        c2.metric("DEPO 그룹 유지 손익", f"{group_prof1:,.0f} 원", delta=f"원가 {group_cost1:,.0f}원", delta_color="off")

        st.success(f"**최종 판단:** {rec1} (상대 선택 대비 **약 {saved1:,.0f}원** 손실 절감 가능)")

        df_sum1 = pd.DataFrame({
            "구분": ["INDV 발권", "DEPO 그룹 유지"],
            "적용 좌석": [f"{pax1}석", f"{depo_seats1}석"],
            "총 매출": [f"{indiv_rev1:,.0f}원", f"{group_rev1:,.0f}원"],
            "총 원가": [f"{indiv_cost1:,.0f}원", f"{group_cost1:,.0f}원"],
            "최종 손익": [f"{indiv_prof1:,.0f}원", f"{group_prof1:,.0f}원"]
        })
        st.dataframe(df_sum1, use_container_width=True, hide_index=True)

        # 6. 노선 기후 & 양국 공휴일 요약 박스
        st.markdown("---")
        st.subheader(f"🗺️ [{route_code1} 노선] 기후 및 달력 특성")
        
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.write(f"🏖️ **노선 기후**: **{season_name1}** ({flight_date1.month}월)")
            st.caption(f"• {season_desc1}")
            
        with col_d2:
            st.write(f"📆 **운항일**: **{flight_date1.strftime('%Y-%m-%d')} ({weekday_kr1})**")
            holiday_tags1 = []
            if is_kr_holiday1: holiday_tags1.append(f"🇰🇷 {kr_holiday_name1}")
            if is_vn_holiday1: holiday_tags1.append(f"🇻🇳 {vn_holiday_name1}")
            
            if holiday_tags1:
                st.warning(f"🎉 **공휴일 태그**: {', '.join(holiday_tags1)}")
            elif is_weekend1:
                st.info(f"🔥 **주말 패턴**: {weekday_kr1} 운항 (주말 출국 선호)")
            else:
                st.caption("💼 일반 주중 평일 패턴")

        # 7. 네이버 항공권 조회 버튼만 바로 표시 (검색 조건 텍스트 박스 삭제 완료)
        st.markdown("---")
        naver_url1 = "https://flight.naver.com/"
        st.markdown(
            f'<a href="{naver_url1}" target="_blank" class="naver-btn">🟢 네이버 항공권 실시간 조회하러 가기 ↗</a>',
            unsafe_allow_html=True
        )

        # 8. AI 종합 전략 리포트
        st.subheader("🤖 AI 종합 전략 리포트 (Comment)")
        
        climate_comment1 = f"• **[{route_code1} {season_name1}]** {season_desc1}"
        if is_dry1:
            climate_comment1 += " (건기 특수로 D-10 시점까지 추가 모객 가능성이 높습니다.)"
        else:
            climate_comment1 += " (우기 시즌이므로 모객 속도가 느릴 수 있으니 무리한 그룹 유지보다는 보수적 대응이 유리합니다.)"

        date_comment1 = []
        if is_kr_holiday1:
            date_comment1.append(f"• **[한국 연휴 특수]** 한국 {kr_holiday_name1} 연휴로 출국 수요 폭증 구간입니다.")
        elif is_weekend1:
            date_comment1.append(f"• **[주말 패턴]** {weekday_kr1} 출발 건으로 주말 선호 모객 우수가 예상됩니다.")
        
        if is_vn_holiday1:
            date_comment1.append(f"• **[베트남 현지 연휴]** 현지 {vn_holiday_name1} 기간으로 현지 지상비 및 인바운드 상황을 체크하세요.")

        date_comment_str1 = "\n".join(date_comment1) if date_comment1 else "• **[일반 날짜]** 특이 공휴일 없는 평일 노선입니다."

        if indiv_prof1 > group_prof1:
            comment_text1 = f"""
**[AI 분석 의견: INDV 전환 강력 권장]**

• **손익분기점 분석:** 현재 실모객({pax1}명)은 손익분기점({bep_pax1:.1f}명) 미달 상태입니다.
• **위험 요인:** DEPO 납입 후 그룹을 유지할 경우 발생할 손실(-{abs(group_prof1):,.0f}원)이 너무 큽니다.
• **비용 절감 효과:** INDV로 전환 발권 시, 그룹 유지 대비 **약 {saved1:,.0f}원**의 손실을 방지(절감)할 수 있습니다.
• 💡 **액션 플랜:** 그룹 블록을 즉시 취소/해제하고 개별 발권을 진행하십시오.

---
**🌤️ 노선 기후 & 🗓️ 공휴일 반영 추가 전략:**
{climate_comment1}
{date_comment_str1}
            """
            st.warning(comment_text1)
        else:
            comment_text1 = f"""
**[AI 분석 의견: DEPO 유지 및 그룹 진행 권장]**

• **손익분기점 분석:** 현재 실모객({pax1}명)이 손익분기점({bep_pax1:.1f}명) 이상이거나, INDV 운임이 매우 비쌉니다.
• **위험 요인:** {depo_seats1}석 전체 운임(-{group_cost1:,.0f}원)을 부담하더라도 그룹을 끌고 가는 것이 손실을 줄이는 길입니다.
• **비용 절감 효과:** INDV 전환 대비 **약 {saved1:,.0f}원**의 비용을 절감할 수 있습니다.
• 💡 **액션 플랜:** DEPO를 납입하여 블록을 유지하고, 남은 D-10(풀페이) 시점까지 추가 모객에 집중하십시오.

---
**🌤️ 노선 기후 & 🗓️ 공휴일 반영 추가 전략:**
{climate_comment1}
{date_comment_str1}
            """
            st.success(comment_text1)


# ==========================================================================
# 📦 [DEPO 후 (GV10 미만) 시뮬레이터]
# ==========================================================================
with tab_sheet2:
    col_input2, col_result2 = st.columns([1, 1.2], gap="large")

    with col_input2:
        st.subheader("📌 [DEPO 후 GV10 미만] 조건 입력")
        st.caption("🔵 **파란색 글씨 입력란** (엑셀과 동일한 계산 구조)")
        
        with st.expander("1️⃣ DEPO 인원 및 기본 NET FARE", expanded=True):
            depo_pax = st.number_input("DEPO 인원 (PAX)", min_value=1, value=10, key="dp_pax")
            depo_net = st.number_input("DEPO 들어가 금액 NET (1인당)", value=405657.10, step=1000.0, format="%.2f", key="dp_net")
            depo_refund = st.number_input("DEPO 환불금 (있을 경우)", value=0.0, step=1000.0, key="dp_ref")

        with st.expander("2️⃣ INDV 발권 시 조건", expanded=True):
            indv_fare = st.number_input("INDV 1인당 NET FARE", value=500000.0, step=10000.0, key="post_ifare")
            indv_pax = st.number_input("INDV 발권 PAX", value=4, key="post_ipax")
            ta1_val = st.number_input("T/A 1 단가 x 인원수 (수입)", value=840000.0, step=10000.0, key="ta1")
            ta2_val = st.number_input("T/A 2 단가 x 인원수 (수입)", value=840000.0, step=10000.0, key="ta2")

        with st.expander("3️⃣ 여행사 마진 / INV 수입 조건", expanded=True):
            inv1_val = st.number_input("INV 1 총액", value=840000.0, step=10000.0, key="inv1")
            inv2_val = st.number_input("INV 2 총액", value=840000.0, step=10000.0, key="inv2")
            inv3_val = st.number_input("INV 3 총액", value=0.0, step=10000.0, key="inv3")

    # [엑셀 수식 계산]
    depo_per_loss = depo_net / 5.0
    depo_total_entry = depo_pax * depo_per_loss
    depo_loss = depo_total_entry - depo_refund

    indv_ticket_total = indv_fare * indv_pax
    indv_plus_depo_loss = indv_ticket_total + depo_loss
    ta_total = ta1_val + ta2_val
    post_indv_total_loss = ta_total - indv_plus_depo_loss

    gv10_ttl = depo_pax * depo_net
    inv_total = inv1_val + inv2_val + inv3_val
    agency_min_cost = gv10_ttl - inv_total
    rem_pax = depo_pax - indv_pax
    min_selling_price_per_pax = agency_min_cost / rem_pax if rem_pax > 0 else 0
    post_ttl_profit = -agency_min_cost

    with col_result2:
        st.subheader("📊 [DEPO 후] 손익 시뮬레이션 리포트")

        st.markdown("##### 1️⃣ INDV 발권할 경우 손익 표")
        df_indv_post = pd.DataFrame({
            "항목": ["DEPO 들어간 금액", "DEPO 환불금", "INDV FARE (발권금)", "INDV 발권금 + DEPO 손실금", "T/A 수입 합계", "총 손익 (최종)"],
            "PAX": [f"{depo_pax}명", "-", f"{indv_pax}명", "-", "-", "-"],
            "금액 (KRW)": [
                f"{depo_total_entry:,.2f} 원",
                f"{depo_refund:,.2f} 원",
                f"{indv_ticket_total:,.2f} 원",
                f"{indv_plus_depo_loss:,.2f} 원",
                f"{ta_total:,.2f} 원",
                f"{post_indv_total_loss:,.2f} 원"
            ]
        })
        st.dataframe(df_indv_post, use_container_width=True, hide_index=True)

        st.markdown("---")

        st.markdown("##### 2️⃣ 여행사 최소 판매 금액 (마진) 계산 표")
        df_margin_post = pd.DataFrame({
            "구분": ["GV10 전체 보장", "F/P TTL (탑업 차감금)", "INV 수입 합계", "여행사 최소 필요 판매가 (1인당)", "TTL 최종 손익 (DEPO 유지)"],
            "PAX / 잔여석": [f"{depo_pax}명", "-", "-", f"잔여 {rem_pax}명", "-"],
            "금액 (KRW)": [
                f"{gv10_ttl:,.2f} 원",
                f"{gv10_ttl:,.2f} 원",
                f"{inv_total:,.2f} 원",
                f"{min_selling_price_per_pax:,.2f} 원",
                f"{post_ttl_profit:,.2f} 원"
            ]
        })
        st.dataframe(df_margin_post, use_container_width=True, hide_index=True)

        st.error(f"🔴 **DEPO 유지 시 잔여 {rem_pax}명**에게 최소 **1인당 {min_selling_price_per_pax:,.0f}원** 이상으로 판매해야 손익분기점(BEP)을 달성할 수 있습니다.")
