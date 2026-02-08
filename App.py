import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="Nu-Finder Oncology", layout="wide")

# 사이드바: 환자 및 데이터 관리
with st.sidebar:
    st.title("🧬 Nu-Finder")
    st.subheader("Patient Intelligence")
    patient_id = st.selectbox("Select Patient", ["PT-8802", "PT-9941", "PT-1023"])
    st.divider()
    uploaded_file = st.file_uploader("Upload NGS Data (FASTA/VCF)")

# 메인 헤더
st.title(f"Oncology Intelligence Report: {patient_id}")
st.caption("AI-Driven Integration of Diagnostics and Therapeutic Design")

# 1열: 주요 지표 (Summary Metrics)
m1, m2, m3, m4 = st.columns(4)
m1.metric("Detected Variants", "12", delta="3 Critical")
m2.metric("AI Prognosis Score", "84%", delta="Positive")
m3.metric("Max PE Efficiency", "92.4%", delta="Optimal")
m4.metric("Off-target Risk", "Low", delta_color="inverse")

st.divider()

# 2열: Triple Check Engine 상세 분석
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("🎯 Layer 3: Prime Editing Strategy")
    # 가상의 pegRNA 편집 효율 데이터
    chart_data = pd.DataFrame({
        "Position": ["-5", "-3", "0", "+3", "+5"],
        "Efficiency": [45, 68, 92, 74, 50],
        "Off-target_Risk": [5, 12, 2, 15, 8]
    })
    
    # 혼합 차트 시각화
    fig = px.line(chart_data, x="Position", y="Efficiency", title="pegRNA Position Optimization", markers=True)
    fig.add_bar(x=chart_data["Position"], y=chart_data["Off-target_Risk"], name="Off-target Risk")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🧪 Layer 1 & 2: Clinical Logic")
    st.info("**Detected Hotspot:** KRAS G12D\n\n**Drug Response:** High sensitivity to Sotorasib")
    
    # 변이 유의성 테이블
    variants = pd.DataFrame({
        "Gene": ["KRAS", "TP53", "APC"],
        "Variant": ["G12D", "R175H", "Q1367*"],
        "Significance": ["Pathogenic", "Likely Pathogenic", "VUS"]
    })
    st.table(variants)

# 3열: 최종 치료 설계 권고안
st.subheader("📝 Therapeutic Design Recommendation")
st.success("""
**Final Strategy:** Use PE7 system with pegRNA-v4.2. 
- **Target Site:** Chr12:25398284 
- **Recommended Action:** MMR suppression required for max efficiency.
""")
