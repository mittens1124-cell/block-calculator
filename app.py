import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(
    page_title="항공 그룹 블록 vs INDV 의사결정 시뮬레이터",
    page_icon="✈️",
    layout="wide"
)

# 2. 커스텀 스타일 적용 (CSS)
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
    </style>
""", unsafe_allow_html=True)

st.title("✈️ 항공 그룹 블록 vs INDV 손익 판단 시뮬레이터")
st.caption("DEPO 전 모객 인원 미달 시, 그룹 유지 vs INDV 전환 손익을 분석하고 AI 전략 코멘트를 제공합니다.")

st.divider()

# 3. 입력 창(좌측)과 결과 창(우측) 2컬럼 레이아웃
col_input, col_result = st.columns([1, 1.2], gap="large")

with col_input:
    st.subheader("📌 조건 입력")
    
    with st.expander("1️⃣ 실모객 및 판매가 설정", expanded=True):
        pax = st.number_input("실모객 인원 (PAX)", min_value=1, max_value=100, value=3, step=1)
        selling_price = st.number_input("1인당 판매가 (KRW)", min_value=0, value=620000, step=10000, format="%d")
        
    with st.expander("2️⃣ INDV 발권 조건", expanded=True):
        indiv_net = st.number_input("INDV 1인당 NET FARE (KRW)", min_value=0, value=1069000, step=10000, format="%d")
        
    with st.expander("3️⃣ DEPO 그룹 조건", expanded=True):
        group_net = st.number_input("그룹 1인당 NET FARE (KRW)", min_value=0.0, value=587457.1, step=1000.0, format="%.2f")
        depo_seats = st.number_input("DEPO 유지/보장 좌석 수", min_value=1, max_value=100, value=11, step=1)

    st.info("💡 **Tip:** 입력을 변경하면 우측의 손익 분석 및 AI Comment가 즉시 자동 계산됩니다.")

# 4. 손익 계산 로직
indiv_revenue = pax * selling_price
indiv_cost = pax * indiv_net
indiv_profit = indiv_revenue - indiv_cost

group_revenue = pax * selling_price
group_cost = depo_seats * group_net
group_profit = group_revenue - group_cost

# 손익분기점(BEP) 인원 계산
bep_pax = (depo_seats * group_net) / indiv_net if indiv_net > 0 else 0

with col_result:
    st.subheader("📊 손익 비교 및 분석 결과")
    
    # 5. 추천 의사결정 판별
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

    # 메트릭 카드 출력
    res_c1, res_c2 = st.columns(2)
    with res_c1:
        st.metric("INDV 발권 시 손익", f"{indiv_profit:,.0f} 원", delta=f"원가 {indiv_cost:,.0f}원", delta_color="off")
    with res_c2:
        st.metric("DEPO 그룹 유지 손익", f"{group_profit:,.0f} 원", delta=f"원가 {group_cost:,.0f}원", delta_color="off")

    st.success(f"**최종 판단:** {recommendation} (상대 선택 대비 **약 {saved_amount:,.0f}원** 손실 절감 가능)")

    # 상세 비교 데이터 프레임
    df_summary = pd.DataFrame({
        "구분": ["INDV 발권", "DEPO 그룹 유지"],
        "적용 좌석": [f"{pax}석", f"{depo_seats}석"],
        "총 매출": [f"{indiv_revenue:,.0f}원", f"{group_revenue:,.0f}원"],
        "총 원가": [f"{indiv_cost:,.0f}원", f"{group_cost:,.0f}원"],
        "최종 손익": [f"{indiv_profit:,.0f}원", f"{group_profit:,.0f}원"]
    })
    st.dataframe(df_summary, use_container_width=True, hide_index=True)

    # 6. AI Comment 생성 및 박스 출력
    st.subheader("🤖 AI 전략 리포트 (Comment)")
    
    if indiv_profit > group_profit:
        comment_text = f"""
**[AI 분석 의견: INDV 전환 강력 권장]**

• **손익분기점 분석:** 현재 실모객({pax}명)은 손익분기점({bep_pax:.1f}명) 미달 상태입니다.
• **위험 요인:** DEPO 납입 후 그룹을 유지할 경우 발생할 손실(-{abs(group_profit):,.0f}원)이 너무 큽니다.
• **비용 절감 효과:** INDV로 전환 발권 시, 그룹 유지 대비 **약 {saved_amount:,.0f}원**의 손실을 방지(절감)할 수 있습니다.
• 💡 **액션 플랜:** 그룹 블록을 즉시 취소/해제하고 개별 발권을 진행하십시오.
        """
        st.warning(comment_text)
    else:
        comment_text = f"""
**[AI 분석 의견: DEPO 유지 및 그룹 진행 권장]**

• **손익분기점 분석:** 현재 실모객({pax}명)이 손익분기점({bep_pax:.1f}명) 이상이거나, INDV 운임이 매우 비쌉니다.
• **위험 요인:** {depo_seats}석 전체 운임(-{group_cost:,.0f}원)을 부담하더라도 그룹을 끌고 가는 것이 손실을 줄이는 길입니다.
• **비용 절감 효과:** INDV 전환 대비 **약 {saved_amount:,.0f}원**의 비용을 절감할 수 있습니다.
• 💡 **액션 플랜:** DEPO를 납입하여 블록을 유지하고, 남은 D-10(풀페이) 시점까지 추가 모객에 집중하십시오.
        """
        st.success(comment_text)
