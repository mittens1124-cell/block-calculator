import datetime
import holidays
import pandas as pd
import streamlit as st

# 1. 페이지 설정
st.set_page_config(
    page_title="베트남 노선 DEPO 전/후 통합 손익 판단 시뮬레이터",
    page_icon="✈️",
    layout="wide",
)

# 2. 커스텀 스타일 (CSS)
st.markdown(
    """
    <style>
    .main { background-color: #f8f9fa; }
    
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
""",
    unsafe_allow_html=True,
)

st.title("✈️ 베트남 노선 그룹 블록 손익 판단 시뮬레이터")
st.caption(
    "상단 탭을 통해 DEPO 전 시뮬레이션과 DEPO 후 (GV10 미만) 손익 계산을"
    " 손쉽게 전환하여 확인하세요."
)

st.divider()

# --------------------------------------------------------------------------
# 📁 시트 탭 구성 (선언)
# --------------------------------------------------------------------------
tab_sheet1, tab_sheet2 = st.tabs(
    ["📋 DEPO 전 시뮬레이터", "📦 DEPO 후 (GV10 미만) 시뮬레이터"]
)

# ==========================================================================
# 📋 [1번 탭] DEPO 전 시뮬레이터
# ==========================================================================
with tab_sheet1:
    col_input1, col_result1 = st.columns([1, 1.2], gap="large")

    with col_input1:
        st.subheader("📌 [DEPO 전] 조건 입력")

        # 1️⃣ 노선 선택
        with st.expander("1️⃣ 노선 선택 (목적지)", expanded=True):
            route_options = ["PQC (푸꾸옥)", "DAD (다낭)", "CXR (나트랑)", "HAN (하노이)", "HPH (하이퐁)", "SAI (씨엠립)"]
            selected_route = st.selectbox(
                "목적지 노선 선택", options=route_options, index=0, key="pre_route"
            )
            route_code1 = selected_route.split(" ")[0]

        # 2️⃣ 출발/운항 날짜 설정
        with st.expander("2️⃣ 출발/운항 날짜 설정", expanded=True):
            flight_date1 = st.date_input(
                "출발/운항 날짜", datetime.date.today(), key="d1"
            )
            month1 = flight_date1.month

            weekday_num1 = flight_date1.weekday()
            weekday_kr1 = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"][
                weekday_num1
            ]
            is_weekend1 = weekday_num1 in [4, 5, 6]

            kr_holidays1 = holidays.KR(years=flight_date1.year)
            vn_holidays1 = holidays.VN(years=flight_date1.year)

            is_kr_holiday1 = flight_date1 in kr_holidays1
            kr_holiday_name1 = (
                kr_holidays1.get(flight_date1) if is_kr_holiday1 else ""
            )

            is_vn_holiday1 = flight_date1 in vn_holidays1
            vn_holiday_name1 = (
                vn_holidays1.get(flight_date1) if is_vn_holiday1 else ""
            )

            # 기후 로직
            is_dry1 = False
            season_name1, season_desc1 = "", ""
            if route_code1 == "PQC":
                is_dry1 = month1 in [11, 12, 1, 2, 3, 4]
                season_name1 = "건기 (최고 성수기)" if is_dry1 else "우기 (비수기)"
                season_desc1 = (
                    "휴양지 특성상 건기 시즌 모객 집중도가 매우 높은 노선입니다."
                    if is_dry1
                    else "우기 시즌으로 강수량이 많아 모객 속도가 더딜 수 있습니다."
                )
            elif route_code1 in ["CXR", "NHA"]:
                is_dry1 = month1 in [1, 2, 3, 4, 5, 6, 7, 8]
                season_name1 = "건기 (성수기)" if is_dry1 else "우기 (우천/태풍 주의)"
                season_desc1 = (
                    "가족/휴양 객단가가 안정적으로 형성되는 시즌입니다."
                    if is_dry1
                    else "Late Rainy Season으로 우천 변동성이 있습니다."
                )
            else:
                is_dry1 = month1 in [1, 2, 3, 4, 11, 12]
                season_name1 = "건기 시즌" if is_dry1 else "우기 시즌"
                season_desc1 = "정규 건기/우기 스케줄에 맞춰 대응하세요."

       # 3️⃣ 실모객 및 판매가 설정 (초기값 0)
        with st.expander("3️⃣ 실모객 및 판매가 설정", expanded=True):
            pax1 = st.number_input(
                "실모객 인원 (PAX)", min_value=0, value=0, step=1, key="pre_pax"
            )
            selling_price1 = st.number_input(
                "1인당 판매가 (KRW)",
                min_value=0.0,
                value=420000.0,
                step=10000.0,
                format="%,d",
                key="pre_price_v2",
            )
        # 4️⃣ INDV 발권 조건 (초기값 0)
        with st.expander("4️⃣ INDV 발권 조건", expanded=True):
            indiv_net1 = st.number_input(
                "INDV 1인당 NET FARE (KRW)",
                min_value=0.0,
                value=0.0,
                step=10000.0,
                format="%.0f",
                key="inet1",
            )

        # 5️⃣ DEPO 그룹 조건 (초기값 0)
        with st.expander("5️⃣ DEPO 그룹 조건", expanded=True):
            group_net1 = st.number_input(
                "그룹 1인당 NET FARE (KRW)",
                min_value=0.0,
                value=0.0,
                step=10000.0,
                format="%.0f",
                key="gnet1",
            )
            depo_seats1 = st.number_input(
                "DEPO 유지/보장 좌석 수",
                min_value=0,
                max_value=100,
                value=0,
                step=1,
                key="gseats1",
            )

    # 연산
    indiv_rev1 = pax1 * selling_price1
    indiv_cost1 = pax1 * indiv_net1
    indiv_prof1 = indiv_rev1 - indiv_cost1

    group_rev1 = pax1 * selling_price1
    group_cost1 = depo_seats1 * group_net1
    group_prof1 = group_rev1 - group_cost1

    bep_pax1 = group_cost1 / selling_price1 if selling_price1 > 0 else 0

    with col_result1:
        st.subheader(f"📊 [{route_code1}] DEPO 전 손익 비교")

        if pax1 == 0 and depo_seats1 == 0:
            st.warning("👈 왼쪽 입력창에서 **실모객 인원 및 조건**을 입력해주시면 시뮬레이션 결과가 표시됩니다.")
        else:
            if indiv_prof1 > group_prof1:
                rec1 = "INDV 발권 전환"
                saved1 = indiv_prof1 - group_prof1
                st.markdown(
                    '<div class="status-badge-indiv">💡 AI 추천: INDV 발권 전환</div>',
                    unsafe_allow_html=True,
                )
            else:
                rec1 = "DEPO 유지 (그룹 진행)"
                saved1 = group_prof1 - indiv_prof1
                st.markdown(
                    '<div class="status-badge-group">💡 AI 추천: DEPO 유지 (그룹 진행)</div>',
                    unsafe_allow_html=True,
                )

            st.write("")
            c1, c2 = st.columns(2)
            c1.metric(
                "INDV 발권 시 손익",
                f"{indiv_prof1:,.0f} 원",
                delta=f"원가 {indiv_cost1:,.0f}원",
                delta_color="off",
            )
            c2.metric(
                "DEPO 그룹 유지 손익",
                f"{group_prof1:,.0f} 원",
                delta=f"원가 {group_cost1:,.0f}원",
                delta_color="off",
            )

            st.success(
                f"**최종 판단:** {rec1} (상대 선택 대비 **약 {saved1:,.0f}원** 손실 절감 가능)"
            )

            df_sum1 = pd.DataFrame({
                "구분": ["INDV 발권", "DEPO 그룹 유지"],
                "적용 좌석": [f"{pax1}석", f"{depo_seats1}석"],
                "총 매출": [f"{indiv_rev1:,.0f}원", f"{group_rev1:,.0f}원"],
                "총 원가": [f"{indiv_cost1:,.0f}원", f"{group_cost1:,.0f}원"],
                "최종 손익": [f"{indiv_prof1:,.0f}원", f"{group_prof1:,.0f}원"],
            })
            st.dataframe(df_sum1, use_container_width=True, hide_index=True)

            st.markdown("---")
            st.subheader(f"🗺️ [{route_code1} 노선] 기후 및 달력 특성")

            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.write(f"🏖️ **노선 기후**: **{season_name1}** ({flight_date1.month}월)")
                st.caption(f"• {season_desc1}")

            with col_d2:
                st.write(
                    "📆 **운항일**:"
                    f" **{flight_date1.strftime('%Y-%m-%d')} ({weekday_kr1})**"
                )
                holiday_tags1 = []
                if is_kr_holiday1:
                    holiday_tags1.append(f"🇰🇷 {kr_holiday_name1}")
                if is_vn_holiday1:
                    holiday_tags1.append(f"🇻🇳 {vn_holiday_name1}")

                if holiday_tags1:
                    st.warning(f"🎉 **공휴일 태그**: {', '.join(holiday_tags1)}")
                elif is_weekend1:
                    st.info(f"🔥 **주말 패턴**: {weekday_kr1} 운항 (주말 출국 선호)")
                else:
                    st.caption("💼 일반 주중 평일 패턴")

            st.markdown("---")
            naver_url1 = "https://flight.naver.com/"
            st.markdown(
                f'<a href="{naver_url1}" target="_blank" class="naver-btn">🟢 네이버 항공권 실시간 조회하러 가기 ↗</a>',
                unsafe_allow_html=True,
            )

            st.subheader("🤖 AI 종합 전략 리포트 (Comment)")

            climate_comment1 = f"• **[{route_code1} {season_name1}]** {season_desc1}"
            if is_dry1:
                climate_comment1 += (
                    " (건기 특수로 D-10 시점까지 추가 모객 가능성이 높습니다.)"
                )
            else:
                climate_comment1 += (
                    " (우기 시즌이므로 모객 속도가 느릴 수 있으니 무리한 그룹 유지보다는 보수적 대응이 유리합니다.)"
                )

            date_comment1 = []
            if is_kr_holiday1:
                date_comment1.append(
                    f"• **[한국 연휴 특수]** 한국 {kr_holiday_name1} 연휴로 출국 수요 폭증 구간입니다."
                )
            elif is_weekend1:
                date_comment1.append(
                    f"• **[주말 패턴]** {weekday_kr1} 출발 건으로 주말 선호 모객 우수가 예상됩니다."
                )

            if is_vn_holiday1:
                date_comment1.append(
                    f"• **[베트남 현지 연휴]** 현지 {vn_holiday_name1} 기간으로 현지 지상비 및 인바운드 상황을 체크하세요."
                )

            date_comment_str1 = (
                "\n".join(date_comment1)
                if date_comment1
                else "• **[일반 날짜]** 특이 공휴일 없는 평일 노선입니다."
            )

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
# 📦 [2번 탭] DEPO 후 시뮬레이터 (최소 판매 요청 인원 수동 입력 버전)
# ==========================================================================
with tab_sheet2:
    col_input2, col_result2 = st.columns([1, 1.2], gap="large")

    with col_input2:
        st.subheader("📌 [DEPO 후] 시뮬레이션 조건 입력")
        st.caption("🔵 모든 단가 및 인원 항목은 기본값으로 설정되어 있습니다.")

        # 1️⃣ DEPO 조건
        with st.expander("1️⃣ DEPO 결제 현황", expanded=True):
            depo_pax = st.number_input(
                "DEPO 전체 인원 (PAX)", min_value=0, value=0, key="dp_pax"
            )
            depo_net = st.number_input(
                "DEPO NET 단가 (KRW)",
                min_value=0.0,
                value=0.0,
                step=1000.0,
                format="%.0f",
                key="dp_net",
            )

        # 2️⃣ Option 1: INDV 발권 전환 조건 & T/A 판매 수입 입력
        with st.expander("2️⃣ [Option 1] INDV 발권 전환 시 조건", expanded=True):
            c_ifare1, c_ifare2, c_ifare3 = st.columns(3)
            indv_fare = c_ifare1.number_input(
                "1인당 NET FARE",
                min_value=0.0,
                value=0.0,
                step=10000.0,
                format="%.0f",
                key="post_ifare",
            )
            indv_baggage = c_ifare2.number_input(
                "수하물 추가금",
                min_value=0.0,
                value=0.0,
                step=5000.0,
                format="%.0f",
                key="post_ibag",
            )
            indv_pax = c_ifare3.number_input(
                "INDV 발권 PAX", min_value=0, value=0, key="post_ipax"
            )

            st.markdown("---")
            st.caption("🛍️ **T/A (여행사) 판매 수입**")

            c_ta1_1, c_ta1_2 = st.columns(2)
            ta1_net = c_ta1_1.number_input(
                "T/A 1 단가", min_value=0.0, value=0.0, step=10000.0, format="%.0f", key="ta1_net"
            )
            ta1_pax = c_ta1_2.number_input(
                "T/A 1 PAX", min_value=0, value=0, key="ta1_pax"
            )

            c_ta2_1, c_ta2_2 = st.columns(2)
            ta2_net = c_ta2_1.number_input(
                "T/A 2 단가", min_value=0.0, value=0.0, step=10000.0, format="%.0f", key="ta2_net"
            )
            ta2_pax = c_ta2_2.number_input(
                "T/A 2 PAX", min_value=0, value=0, key="ta2_pax"
            )

            c_ta3_1, c_ta3_2 = st.columns(2)
            ta3_net = c_ta3_1.number_input(
                "T/A 3 단가", min_value=0.0, value=0.0, step=10000.0, format="%.0f", key="ta3_net"
            )
            ta3_pax = c_ta3_2.number_input(
                "T/A 3 PAX", min_value=0, value=0, key="ta3_pax"
            )

        # 3️⃣ Option 2: 그룹 블록 유지 조건 (사용자 지정 요청 인원 추가)
        with st.expander(
            "3️⃣ [Option 2] 그룹 블록 유지 시 조건", expanded=True
        ):
            # ✏️ [신규 추가] 사용자가 직접 입력하는 판매 요청 인원
            req_pax = st.number_input(
                "여행사 최소 판매 요청 인원 (PAX)",
                min_value=0,
                value=0,
                key="opt2_req_pax",
                help="1인당 최소 판매 필요 금액을 산출할 요청 인원을 직접 입력하세요."
            )

            st.markdown("---")
            st.info(
                "💡 **T/A 1, T/A 2, T/A 3 조건은 위 [Option 1]에서 입력한 값과 연동됩니다.**"
            )
            st.markdown(
                f"- **T/A 1**: `{ta1_net:,.0f}원` / `{ta1_pax}명`\n"
                f"- **T/A 2**: `{ta2_net:,.0f}원` / `{ta2_pax}명`\n"
                f"- **T/A 3**: `{ta3_net:,.0f}원` / `{ta3_pax}명`"
            )

    # ----------------------------------------------------------------------
    # 🧮 연산 수식
    # ----------------------------------------------------------------------
    # DEPO 20% 단가
    depo_per_pax = depo_net * 0.20
    depo_total_entry = depo_per_pax * depo_pax

    # T/A 수입 합계
    ta1_ttl = ta1_net * ta1_pax
    ta2_ttl = ta2_net * ta2_pax
    ta3_ttl = ta3_net * ta3_pax
    ta_total_revenue = ta1_ttl + ta2_ttl + ta3_ttl

    # ======================================================================
    # 🎯 구간별 환불 가능 인원 판정
    # ======================================================================
    if depo_pax >= 35:
        depo_refund_pax = 4
    elif depo_pax >= 25:
        depo_refund_pax = 3
    elif depo_pax >= 15:
        depo_refund_pax = 2
    elif depo_pax >= 11:
        depo_refund_pax = 1
    else:
        depo_refund_pax = 0

    depo_refund_amount = depo_refund_pax * depo_per_pax

    # ======================================================================
    # 🔵 [Option 1 연산] - INDV 전환
    # ======================================================================
    opt1_refund_pax = depo_refund_pax
    opt1_refund_amount = depo_refund_amount
    depo_loss_a = depo_total_entry - opt1_refund_amount
    indv_ticket_ttl = (indv_fare + indv_baggage) * indv_pax

    indv_plus_depo_cost = indv_ticket_ttl + depo_loss_a
    indv_plus_depo_val = -indv_plus_depo_cost

    path_a_net_profit = ta_total_revenue - indv_plus_depo_cost

    # ======================================================================
    # 🟢 [Option 2 연산] - 그룹 블록 유지
    # ======================================================================
    gv10_pax = 10
    gv10_total_amount = gv10_pax * depo_net

    if depo_pax > gv10_pax:
        depo_non_refund_pax = max(0, depo_pax - gv10_pax - depo_refund_pax)
    else:
        depo_non_refund_pax = 0
    
    depo_non_refund_amount = depo_non_refund_pax * depo_per_pax

    # F/P TTL = GV10 원가 - DEPO 환불금 + DEPO 환불불가금
    fp_ttl = gv10_total_amount - depo_refund_amount + depo_non_refund_amount

    # TTL 손익
    path_b_ttl_profit = ta_total_revenue - fp_ttl

    # ✏️ [수정] 사용자가 직접 입력한 req_pax 기준 1인당 최소 판매 요청 금액 산출
    if req_pax > 0:
        min_selling_price_b = (
            abs(path_b_ttl_profit) / req_pax
            if path_b_ttl_profit < 0
            else 0.0
        )
    else:
        min_selling_price_b = 0.0

    # ----------------------------------------------------------------------
    # 🎨 데이터프레임 조건부 스타일링 함수 (손익 색상)
    # ----------------------------------------------------------------------
    def style_dataframe(df):
        def color_cells(val):
            if isinstance(val, str):
                if val.startswith("-"):
                    return "color: #E53E3E; font-weight: bold;"
                elif val.startswith("+"):
                    return "color: #3182CE; font-weight: bold;"
            return ""

        return df.style.map(color_cells)

    # ----------------------------------------------------------------------
    # 📊 결과 출력
    # ----------------------------------------------------------------------
    with col_result2:
        st.subheader("📊 DEPO 후 최종 의사결정 시뮬레이션")

        if depo_pax == 0:
            st.warning(
                "👈 왼쪽 입력창에서 **DEPO 인원 및 조건**을 입력해주시면 시뮬레이션 비교 결과가 표시됩니다."
            )
        else:
            # 추천 조건 비교
            if path_a_net_profit > path_b_ttl_profit:
                st.success(
                    "💡 **시뮬레이션 추천: [Option 1] INDV 발권 전환 유효**\n\n"
                    f"* **Option 1 손익**: `{path_a_net_profit:,.0f}원`\n"
                    f"* **Option 2 손익**: `{path_b_ttl_profit:,.0f}원`\n\n"
                    f"👉 INDV 전환이 현시점 그룹 블록 유지 대비 **{abs(path_a_net_profit - path_b_ttl_profit):,.0f}원** 손익이 우수합니다."
                )
            else:
                st.info(
                    "💡 **시뮬레이션 추천: [Option 2] 그룹 블록 유지 및 운영 유효**\n\n"
                    f"* **Option 2 입력 요청인원 ({req_pax}명) 최소 판매 필요 단가**: `{min_selling_price_b:,.0f}원`\n"
                    f"👉 요청하신 **{req_pax}명**을 1인당 **{min_selling_price_b:,.0f}원 이상**으로 판매 시 손실을 완전 상쇄할 수 있습니다."
                )

            st.markdown("---")

            # ==================================================================
            # 1️⃣ [Option 1] 결과 출력
            # ==================================================================
            st.markdown("##### 1️⃣ [Option 1] INDV 발권 전환 손익표")

            summary_val_str1 = f"+{path_a_net_profit:,.0f} 원" if path_a_net_profit > 0 else f"{path_a_net_profit:,.0f} 원"

            df_a_summary = pd.DataFrame({
                "항목": ["총 손익"],
                "PAX": ["-"],
                "NET / 단가": ["-"],
                "금액 (KRW)": [summary_val_str1]
            })
            st.dataframe(style_dataframe(df_a_summary), use_container_width=True, hide_index=True)

            with st.expander("🔍 [Option 1] 세부 내역 보기 / 접기", expanded=False):
                df_a_detail = pd.DataFrame({
                    "항목": [
                        "DEPO 들어간 금액",
                        "DEPO 환불금",
                        "DEPO 손실액",
                        "INDV FARE",
                        "INDV 발권금 + DEPO 손실금",
                        "T/A 1 수입",
                        "T/A 2 수입",
                        "T/A 3 수입",
                        "총 손익"
                    ],
                    "PAX": [
                        f"{depo_pax}명",
                        f"{opt1_refund_pax}명",
                        f"{max(0, depo_pax - opt1_refund_pax)}명",
                        f"{indv_pax}명",
                        "-",
                        f"{ta1_pax}명",
                        f"{ta2_pax}명",
                        f"{ta3_pax}명",
                        "-"
                    ],
                    "NET / 단가": [
                        f"{depo_net:,.0f}원",
                        f"{depo_net:,.0f}원",
                        "-",
                        f"{indv_fare:,.0f}원",
                        "-",
                        f"{ta1_net:,.0f}원",
                        f"{ta2_net:,.0f}원",
                        f"{ta3_net:,.0f}원",
                        "-"
                    ],
                    "금액 (KRW)": [
                        f"{depo_total_entry:,.0f} 원",
                        f"{opt1_refund_amount:,.0f} 원",
                        f"-{depo_loss_a:,.0f} 원",
                        f"{indv_ticket_ttl:,.0f} 원",
                        f"{indv_plus_depo_val:,.0f} 원",
                        f"+{ta1_ttl:,.0f} 원" if ta1_ttl > 0 else "0 원",
                        f"+{ta2_ttl:,.0f} 원" if ta2_ttl > 0 else "0 원",
                        f"+{ta3_ttl:,.0f} 원" if ta3_ttl > 0 else "0 원",
                        summary_val_str1
                    ]
                })
                st.dataframe(style_dataframe(df_a_detail), use_container_width=True, hide_index=True)

            st.markdown("---")

            # ==================================================================
            # 2️⃣ [Option 2] 결과 출력 (수동 입력 req_pax 반영)
            # ==================================================================
            st.markdown("##### 2️⃣ [Option 2] 여행사 최소 판매 금액 / 블록 유지 (ABS 적용)")

            summary_val_str2 = f"+{path_b_ttl_profit:,.0f} 원" if path_b_ttl_profit > 0 else f"{path_b_ttl_profit:,.0f} 원"

            df_b_summary = pd.DataFrame({
                "구분 / 항목": ["여행사 최소 판매 요청 금액", "TTL 손익"],
                "PAX": [f"🌸 {req_pax}명", "-"],
                "NET / 단가": [f"{min_selling_price_b:,.0f}원", "-"],
                "TTL (금액)": ["-", summary_val_str2]
            })
            st.dataframe(style_dataframe(df_b_summary), use_container_width=True, hide_index=True)

            with st.expander("🔍 [Option 2] 세부 내역 보기 / 접기", expanded=True):
                df_b_detail = pd.DataFrame({
                    "구분 / 항목": [
                        "GV10 원가",
                        "DEPO 환불 가능",
                        "DEPO 환불 불가",
                        "F/P TTL (탑업 차감금)",
                        "T/A 1 판매",
                        "T/A 2 판매",
                        "T/A 3 판매",
                        "여행사 최소 판매 요청 금액",
                        "TTL 손익"
                    ],
                    "PAX": [
                        f"{gv10_pax}명",
                        f"{depo_refund_pax}명",
                        f"{depo_non_refund_pax}명",
                        "-",
                        f"{ta1_pax}명",
                        f"{ta2_pax}명",
                        f"{ta3_pax}명",
                        f"🌸 {req_pax}명",
                        "-"
                    ],
                    "NET / 단가": [
                        f"{depo_net:,.0f}원",
                        f"{depo_net:,.0f}원",
                        f"{depo_net:,.0f}원",
                        "-",
                        f"{ta1_net:,.0f}원",
                        f"{ta2_net:,.0f}원",
                        f"{ta3_net:,.0f}원",
                        f"{min_selling_price_b:,.0f}원",
                        "-"
                    ],
                    "TTL (금액)": [
                        f"{gv10_total_amount:,.0f} 원",
                        f"{depo_refund_amount:,.0f} 원",
                        f"{depo_non_refund_amount:,.0f} 원",
                        f"-{fp_ttl:,.0f} 원",
                        f"+{ta1_ttl:,.0f} 원" if ta1_ttl > 0 else "0 원",
                        f"+{ta2_ttl:,.0f} 원" if ta2_ttl > 0 else "0 원",
                        f"+{ta3_ttl:,.0f} 원" if ta3_ttl > 0 else "0 원",
                        "-",
                        summary_val_str2
                    ]
                })
                st.dataframe(style_dataframe(df_b_detail), use_container_width=True, hide_index=True)

            st.markdown("---")
            st.subheader("🤖 AI 종합 전략 리포트 (Comment)")

            if path_a_net_profit > path_b_ttl_profit:
                comment_text2 = f"""
**[AI 분석 의견: Option 1 개별(INDV) 발권 전환 추천]**

• **손익 분석:** Option 1의 예상 손익({path_a_net_profit:,.0f}원)이 Option 2 유지 시 손익({path_b_ttl_profit:,.0f}원)보다 우수합니다.
• **절감 효과:** INDV 발권으로 전환 시 그룹 유지 대비 **약 {abs(path_a_net_profit - path_b_ttl_profit):,.0f}원**의 손익 개선 효과를 얻을 수 있습니다.
• 💡 **액션 플랜:** 미판매 잔여석 모객 부담을 해소하기 위해 그룹 블록을 해제하고 INDV 개별 발권으로 즉시 전환하십시오.
"""
                st.warning(comment_text2)
            else:
                comment_text2 = f"""
**[AI 분석 의견: Option 2 그룹 블록 유지 및 추가 모객 추천]**

• **손익 분석:** GV10 보장 조건을 활용하여 그룹 블록을 끌고 가는 것이 상대적으로 유리합니다.
• **목표 단가:** 요청하신 **{req_pax}석**에 대해 1인당 최소 **{min_selling_price_b:,.0f}원 이상**으로 판매를 완료할 경우 손실을 완전 상쇄(BEP 달성)할 수 있습니다.
• 💡 **액션 플랜:** T/A 및 프로모션 채널을 통해 요청 {req_pax}석에 대한 땡처리 또는 타겟 영업 전략을 강화하십시오.
"""
                st.success(comment_text2)

