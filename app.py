import pandas as pd
import streamlit as st

# ==========================================================================
# 📦 [DEPO 후 시뮬레이터] - 들여쓰기 완벽 수정본
# ==========================================================================
with tab_sheet2:
  col_input2, col_result2 = st.columns([1, 1.2], gap="large")

  with col_input2:
    st.subheader("📌 [DEPO 후] 시뮬레이션 조건 입력")
    st.caption("🔵 모든 단가 및 인원 항목은 **0**으로 기본 설정되어 있습니다.")

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
          format="%.2f",
          key="dp_net",
      )

    # 2️⃣ 경로 A: INDV 발권 전환 조건
    with st.expander("2️⃣ [경로 A] INDV 발권 전환 시 조건", expanded=True):
      c_ifare1, c_ifare2, c_ifare3 = st.columns(3)
      indv_fare = c_ifare1.number_input(
          "1인당 NET FARE",
          min_value=0.0,
          value=0.0,
          step=10000.0,
          key="post_ifare",
      )
      indv_baggage = c_ifare2.number_input(
          "수하물 추가금",
          min_value=0.0,
          value=0.0,
          step=5000.0,
          key="post_ibag",
      )
      indv_pax = c_ifare3.number_input(
          "INDV 발권 PAX", min_value=0, value=0, key="post_ipax"
      )

      st.markdown("---")
      st.caption("🛍️ **T/A (여행사) 판매 수입**")
      c_ta1_1, c_ta1_2 = st.columns(2)
      ta1_net = c_ta1_1.number_input(
          "T/A 1 단가", min_value=0.0, value=0.0, step=10000.0, key="ta1_net"
      )
      ta1_pax = c_ta1_2.number_input(
          "T/A 1 PAX", min_value=0, value=0, key="ta1_pax"
      )

      c_ta2_1, c_ta2_2 = st.columns(2)
      ta2_net = c_ta2_1.number_input(
          "T/A 2 단가", min_value=0.0, value=0.0, step=10000.0, key="ta2_net"
      )
      ta2_pax = c_ta2_2.number_input(
          "T/A 2 PAX", min_value=0, value=0, key="ta2_pax"
      )

    # 3️⃣ 경로 B: 그룹 블록 유지 조건
    with st.expander(
        "3️⃣ [경로 B] 그룹 블록 유지 시 조건 (INV 수입)", expanded=True
    ):
      c_inv1_1, c_inv1_2 = st.columns(2)
      inv1_net = c_inv1_1.number_input(
          "INV 1 단가 (NET)",
          min_value=0.0,
          value=0.0,
          step=10000.0,
          key="inv1_net",
      )
      inv1_pax = c_inv1_2.number_input(
          "INV 1 인원 (PAX)", min_value=0, value=0, key="inv1_pax"
      )

      c_inv2_1, c_inv2_2 = st.columns(2)
      inv2_net = c_inv2_1.number_input(
          "INV 2 단가 (NET)",
          min_value=0.0,
          value=0.0,
          step=10000.0,
          key="inv2_net",
      )
      inv2_pax = c_inv2_2.number_input(
          "INV 2 인원 (PAX)", min_value=0, value=0, key="inv2_pax"
      )

      c_inv3_1, c_inv3_2 = st.columns(2)
      inv3_net = c_inv3_1.number_input(
          "INV 3 단가 (NET)",
          min_value=0.0,
          value=0.0,
          step=10000.0,
          key="inv3_net",
      )
      inv3_pax = c_inv3_2.number_input(
          "INV 3 인원 (PAX)", min_value=0, value=0, key="inv3_pax"
      )

  # ----------------------------------------------------------------------
  # 🧮 연산 수식
  # ----------------------------------------------------------------------
  # 1. DEPO 공통 계산
  depo_per_pax = depo_net * 0.20  # 1인당 DEPO
  depo_total_entry = depo_per_pax * depo_pax  # DEPO 전체 금액

  # LOOKUP 환불 인원
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

  depo_refund_amount = depo_refund_pax * depo_per_pax  # DEPO 환불 가능금

  # --- [경로 A 수식] INDV 발권 전환 ---
  depo_loss_a = depo_total_entry - depo_refund_amount  # DEPO 손실액
  indv_ticket_ttl = (indv_fare + indv_baggage) * indv_pax  # INDV FARE
  indv_plus_depo = (
      indv_ticket_ttl + depo_loss_a
  )  # INDV 발권금 + DEPO 손실금
  ta1_ttl = ta1_net * ta1_pax
  ta2_ttl = ta2_net * ta2_pax
  path_a_total_loss = (
      ta1_ttl + ta2_ttl
  ) - indv_plus_depo  # 경로 A 총 손실 (음수)

  # --- [경로 B 수식] 그룹 블록 유지 ---
  gv10_pax = 10
  gv10_total_amount = gv10_pax * depo_net  # GV10 10명 원가

  depo_non_refund_pax = (
      max(0, depo_pax - gv10_pax - depo_refund_pax)
      if depo_pax >= gv10_pax
      else 0
  )
  depo_non_refund_amount = (
      depo_non_refund_pax * depo_per_pax
  )  # DEPO 환불 불가 금액

  # F/P TTL = GV10 원가 + 환불 가능액 + 환불 불가액
  fp_ttl = gv10_total_amount + depo_refund_amount + depo_non_refund_amount

  inv1_ttl = inv1_net * inv1_pax
  inv2_ttl = inv2_net * inv2_pax
  inv3_ttl = inv3_net * inv3_pax
  inv_total_revenue = inv1_ttl + inv2_ttl + inv3_ttl  # INV 수입 합계

  sold_pax = inv1_pax + inv2_pax + inv3_pax  # 이미 판매된 인원
  remaining_pax = max(0, gv10_pax - sold_pax)  # 남은 소진 필요 인원

  path_b_ttl_profit = inv_total_revenue - fp_ttl  # TTL 손익

  # ABS 기반 남은 좌석 최소 판매 요청 금액
  if remaining_pax > 0:
    min_selling_price_b = abs(path_b_ttl_profit) / remaining_pax
  else:
    min_selling_price_b = 0.0

  # ----------------------------------------------------------------------
  # 📊 시뮬레이션 결과 및 비교 판단
  # ----------------------------------------------------------------------
  with col_result2:
    st.subheader("📊 DEPO 후 최종 의사결정 시뮬레이션")

    if depo_pax == 0:
      st.warning(
          "👈 왼쪽 입력창에서 **DEPO 인원 및 조건**을 입력해주시면 시뮬레이션"
          " 비교 결과가 표시됩니다."
      )
    else:
      if path_a_total_loss > path_b_ttl_profit:
        st.success(
            "💡 **시뮬레이션 추천: [경로 A] INDV 발권 전환 유효**\n\n"
            f"* **경로 A 손익**: `{path_a_total_loss:,.2f}원`\n"
            f"* **경로 B 현 손익**: `{path_b_ttl_profit:,.2f}원`\n\n"
            "👉 INDV 전환이 현시점 그룹 블록 유지 대비"
            f" **{abs(path_a_total_loss - path_b_ttl_profit):,.2f}원** 손실을"
            " 줄일 수 있습니다."
        )
      else:
        st.info(
            "💡 **시뮬레이션 추천: [경로 B] 그룹 블록 유지 및 운영 유효**\n\n"
            f"* **경로 B 남은 {remaining_pax}석 최소 판매 필요 단가**:"
            f" `{min_selling_price_b:,.2f}원`\n"
            f"👉 나머지 {remaining_pax}석을 1인당"
            f" **{min_selling_price_b:,.2f}원 이상**으로 판매 시 경로 A보다"
            " 유효하거나 손실을 완전 상쇄할 수 있습니다."
        )

    st.markdown("---")

    # 1️⃣ 경로 A 표
    st.markdown("##### 1️⃣ [경로 A] INDV 발권 전환 손익표")
    loss_display_a = (
        f":red[**{path_a_total_loss:,.2f} 원**]"
        if path_a_total_loss < 0
        else f"{path_a_total_loss:,.2f} 원"
    )

    df_a = pd.DataFrame({
        "항목": [
            "DEPO 들어간 금액",
            "DEPO 환불금",
            "DEPO 손실액",
            "INDV FARE",
            "INDV 발권금 + DEPO 손실금",
            "T/A 1 수입",
            "T/A 2 수입",
            "총 손실",
        ],
        "PAX": [
            f"{depo_pax}명",
            f"{depo_refund_pax}명",
            f"{max(0, depo_pax-depo_refund_pax)}명",
            f"{indv_pax}명",
            "-",
            f"{ta1_pax}명",
            f"{ta2_pax}명",
            "-",
        ],
        "NET / 단가": [
            f"{depo_net:,.2f}원",
            "-",
            "-",
            f"{indv_fare:,.2f}원",
            "-",
            f"{ta1_net:,.2f}원",
            f"{ta2_net:,.2f}원",
            "-",
        ],
        "금액 (KRW)": [
            f"{depo_total_entry:,.2f} 원",
            f"{depo_refund_amount:,.2f} 원",
            f"{depo_loss_a:,.2f} 원",
            f"{indv_ticket_ttl:,.2f} 원",
            f":red[**{indv_plus_depo:,.2f} 원**]",
            f"{ta1_ttl:,.2f} 원",
            f"{ta2_ttl:,.2f} 원",
            loss_display_a,
        ],
    })
    st.dataframe(df_a, use_container_width=True, hide_index=True)

    st.markdown("---")

    # 2️⃣ 경로 B 표
    st.markdown("##### 2️⃣ [경로 B] 여행사 최소 판매 금액 / 블록 유지 (ABS 적용)")
    loss_display_b = (
        f":red[**{path_b_ttl_profit:,.2f} 원**]"
        if path_b_ttl_profit < 0
        else f"{path_b_ttl_profit:,.2f} 원"
    )

    df_b = pd.DataFrame({
        "구분 / 항목": [
            "GV10 원가",
            "DEPO 환불 가능",
            "DEPO 환불 불가",
            "F/P TTL (탑업 차감금)",
            "INV 1 판매",
            "INV 2 판매",
            "INV 3 판매",
            "여행사 최소 판매 요청 금액",
            "TTL 손익",
        ],
        "PAX": [
            f"{gv10_pax}명",
            f"{depo_refund_pax}명",
            f"{depo_non_refund_pax}명",
            "-",
            f"{inv1_pax}명",
            f"{inv2_pax}명",
            f"{inv3_pax}명",
            f"🌸 **{remaining_pax}명**",
            "-",
        ],
        "NET / 단가": [
            f"{depo_net:,.2f}원",
            f"{depo_net:,.2f}원",
            f"{depo_net:,.2f}원",
            "-",
            f"{inv1_net:,.2f}원",
            f"{inv2_net:,.2f}원",
            f"{inv3_net:,.2f}원",
            f":red[**{min_selling_price_b:,.2f}원**]",
            "-",
        ],
        "TTL (금액)": [
            f"{gv10_total_amount:,.2f} 원",
            f"{depo_refund_amount:,.2f} 원",
            f"{depo_non_refund_amount:,.2f} 원",
            f"**{fp_ttl:,.2f} 원**",
            f"{inv1_ttl:,.2f} 원",
            f"{inv2_ttl:,.2f} 원",
            f"{inv3_ttl:,.2f} 원",
            "-",
            loss_display_b,
        ],
    })
    st.dataframe(df_b, use_container_width=True, hide_index=True)
