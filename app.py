import streamlit as st
import pandas as pd
import datetime
import holidays

# 페이지 설정
st.set_page_config(page_title="베트남 노선 블록 손익 계산기", page_icon="✈️", layout="wide")

st.title("✈️ 베트남 노선 블록 손익 & 수요 예측 계산기")
st.write("운항 날짜를 선택하시면 **한국 및 베트남 공휴일**과 요일 특성을 통합 분석하여 손익을 예측합니다.")

st.markdown("---")

# 1. 날짜 및 조건 입력 섹션
col_date, col_base = st.columns(2)

with col_date:
    st.subheader("📅 운항 날짜 선택")
    selected_date = st.date_input("운항/판매 날짜", datetime.date.today())
    
    # 요일 판별
    weekday_num = selected_date.weekday() # 0:월 ~ 6:일
    weekday_kr = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"][weekday_num]
    is_weekend = weekday_num in [4, 5, 6] # 금, 토, 일

    # 🇻🇳 한국(KR) & 베트남(VN) 공휴일 자동 조회
    kr_holidays = holidays.KR(years=selected_date.year)
    vn_holidays = holidays.VN(years=selected_date.year)

    is_kr_holiday = selected_date in kr_holidays
    kr_holiday_name = kr_holidays.get(selected_date) if is_kr_holiday else ""

    is_vn_holiday = selected_date in vn_holidays
    vn_holiday_name = vn_holidays.get(selected_date) if is_vn_holiday else ""

with col_base:
    st.subheader("⚙️ 기본 조건 입력")
    total_seats = st.number_input("전체 블록 좌석 수 (석)", min_value=1, value=100, step=10)
    seat_cost = st.number_input("좌석당 원가 (원)", min_value=0, value=150000, step=10000)
    seat_price = st.number_input("좌석당 판매가 (원)", min_value=0, value=200000, step=10000)

# 2. 요일 및 양국 공휴일 자동 분석 리포트
st.markdown("---")
st.subheader("📊 양국 공휴일 & 요일 특성 자동 분석")

base_lf = 70.0 # 기본 탑승/판매율 (%)
bonus_lf = 0.0

col_info1, col_info2 = st.columns(2)

with col_info1:
    st.write(f"📆 **선택한 날짜**: **{selected_date.strftime('%Y-%m-%d')} ({weekday_kr})**")
    
    # 🇰🇷 한국 공휴일 판단 (수요 영향 핵심)
    if is_kr_holiday:
        st.success(f"🇰🇷 **[한국 공휴일] {kr_holiday_name}**: 한국 출국 수요 폭증 구간 (판매율 +20%p 반영)")
        bonus_lf += 20.0
    elif is_weekend:
        st.warning(f"🔥 **[주말 효과] {weekday_kr}**: 주말 출국 선호로 평일 대비 수요 우수 (판매율 +10%p 반영)")
        bonus_lf += 10.0
    else:
        st.write(f"💼 **[평일 운항]**: 일반 평일({weekday_kr}) 노선입니다.")

    # 🇻🇳 베트남 공휴일 판단 (현지 상황 코멘트)
    if is_vn_holiday:
        st.info(f"🇻🇳 **[베트남 공휴일] {vn_holiday_name}**: 현지 연휴 기간입니다. (현지 지상비/호텔 비용 상승 및 현지 인바운드 수요 체크 필요)")

with col_info2:
    est_lf = min(100.0, base_lf + bonus_lf)
    st.metric(label="📈 예측 블록 판매율 (L/F)", value=f"{est_lf:.1f}%", delta=f"{bonus_lf:+.1f}%p (날짜 가산 효과)")

# 3. 손익 계산
st.markdown("---")
st.subheader("💰 손익 시뮬레이션 결과")

est_sold_seats = int(total_seats * (est_lf / 100))
total_revenue = est_sold_seats * seat_price
total_cost = total_seats * seat_cost
profit = total_revenue - total_cost

col_r1, col_r2, col_r3 = st.columns(3)
col_r1.metric("총 예상 매출", f"{total_revenue:,} 원")
col_r2.metric("총 블록 비용", f"{total_cost:,} 원")
col_r3.metric("예상 영업손익", f"{profit:,} 원", delta=f"{profit:,} 원")

# 종합 코멘트 박스
st.markdown("### 💡 종합 운영 및 손익 코멘트")

comment_text = []

if is_kr_holiday and is_vn_holiday:
    comment_text.append(f"• **양국 동시 연휴 특수**: 한국({kr_holiday_name})과 베트남({vn_holiday_name})이 모두 공휴일인 극성수기 구간입니다. 최상위 단가 판매 전략을 추천합니다.")
elif is_kr_holiday:
    comment_text.append(f"• **한국 연휴 특수**: {kr_holiday_name} 효과로 한국발 출국 수요가 매우 강합니다. 만석 달성이 무난할 것으로 예상됩니다.")
elif is_vn_holiday:
    comment_text.append(f"• **베트남 연휴 주의**: {vn_holiday_name} 기간으로, 베트남 현지 행사/휴무로 인한 지상 세팅 및 현지 인바운드 수요를 점검하세요.")

if profit > 0:
    st.balloons()
    st.success(f"✅ **흑자 예상 ({profit:,}원)**\n\n" + "\n".join(comment_text))
else:
    st.error(f"⚠️ **적자 예상 ({abs(profit):,}원)**\n\n" + "\n".join(comment_text) + "\n• 현재 예측 판매율로는 손실이 발생하므로 모객 프로모션이나 판매가 재설정이 필요합니다.")
