import streamlit as st
import pandas as pd
import io
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction, MeltingTemp as mt

# --- [Core Logic] 논문 근거 기반 엔진 ---
def analyze_genomic_logic(sequence, edit_length):
    """
    입력된 서열의 물리적 특성과 논문의 PE-SB 효율 로직을 연산합니다.
    """
    # 1. 생물학적 수치 연산 (BioPython 활용)
    gc_val = gc_fraction(sequence) * 100
    tm_val = mt.Tm_NN(sequence)  # Nearest-neighbor 방식의 결합 온도 계산
    
    # 2. 논문(PE7-SB2) 기반 개선율 수식화
    # 12bp 이하일 때 MMR 억제 효과(18.8배)가 극대화된다는 논문 데이터 반영
    if edit_length <= 12:
        boost_factor = 18.8
        status = "MMR Path Inhibited (Optimal)"
    else:
        boost_factor = 1.2
        status = "MMR Interference Likely"

    # 3. 종합 편집 점수 (GC 함량 40-60%를 최적으로 상정한 가중치 모델)
    stability = 1.0 - (abs(50 - gc_val) / 50)
    efficiency_score = (stability * 100) * (boost_factor / 18.8)
    
    return {
        "GC (%)": round(gc_val, 2),
        "Tm (°C)": round(tm_val, 2),
        "PE-SB Score": round(efficiency_score, 2),
        "Analysis": status
    }

# --- [UI] Streamlit 인터페이스 ---
st.set_page_config(page_title="Nu-Finder Oncology AI", layout="wide")
st.title("🧬 Nu-Finder Oncology AI")
st.markdown("### **Dynamic Analysis Engine v2.0**")
st.info("호륜 님의 피드백을 반영하여 데이터 연산 로직이 강화된 버전입니다.")

# 파일 업로더
uploaded_file = st.file_uploader("분석할 유전자 데이터(FASTA)를 업로드하세요.", type=['fasta', 'fa'])

if uploaded_file:
    # 1. 데이터 로드 (BioPython)
    stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
    records = list(SeqIO.parse(stringio, "fasta"))
    
    if records:
        # 사용자로부터 편집 길이 입력 받음 (연산의 핵심 변수)
        edit_len = st.number_input("희망 편집 길이 (Edit Length, bp)", min_value=1, max_value=100, value=5)
        
        results_list = []
        for r in records:
            # 핵심 엔진 가동
            analysis = analyze_genomic_logic(str(r.seq), edit_len)
            analysis['ID'] = r.id
            results_list.append(analysis)
        
        df = pd.DataFrame(results_list)
        
        # 2. 결과 시각화
        st.divider()
        st.subheader("📊 실시간 분석 결과 (Computed Data)")
        
        # 데이터 프레임 출력
        st.dataframe(df[['ID', 'GC (%)', 'Tm (°C)', 'PE-SB Score', 'Analysis']], use_container_width=True)
        
        # 동적 그래프 (입력값에 따라 실시간 변화)
        c1, c2 = st.columns(2)
        with c1:
            st.write("**Target별 예측 효율 (PE-SB Score)**")
            st.bar_chart(df.set_index('ID')['PE-SB Score'])
        with c2:
            st.write("**서열 안정성 지표 (Melting Temperature)**")
            st.line_chart(df.set_index('ID')['Tm (°C)'])
            
        # 3. 전문가 가이드라인
        st.subheader("💡 Nu-Logic Expertise")
        avg_score = df['PE-SB Score'].mean()
        if avg_score > 70:
            st.success(f"현재 평균 효율 점수는 {avg_score:.1f}점입니다. PE7-SB2 플랫폼 도입 시 높은 성공률이 기대됩니다.")
        else:
            st.warning(f"평균 점수가 {avg_score:.1f}점으로 낮습니다. 가이드 RNA의 GC 함량이나 편집 길이를 재검토하십시오.")

    else:
        st.error("올바른 FASTA 형식의 데이터가 아닙니다.")
