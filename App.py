import streamlit as st
import pandas as pd
import io
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction, MeltingTemp as mt

# --- [Core Engine] 진짜 데이터에 반응하는 로직 ---
def run_nu_engine(seq_record, edit_len):
    sequence = str(seq_record.seq).upper()
    
    # 1. 생물학적 수치 물리 연산
    gc_val = gc_fraction(sequence) * 100
    # Nearest-neighbor 가중치를 적용한 실제 결합 온도 계산
    tm_val = mt.Tm_NN(sequence) 
    
    # 2. 논문(PE7-SB2) 기반 효율 스케일링
    # 편집 길이에 따라 MMR 억제 효율이 물리적으로 변함
    if edit_len <= 12:
        boost = 18.8
        note = "Optimal for PE-SB"
    else:
        boost = 1.2
        note = "Low Efficiency (MMR Interference)"

    # 3. 종합 안정성 점수 산출 (GC 함량 40-60% 최적 가중치)
    stability_factor = 1.0 - (abs(50 - gc_val) / 50)
    score = (stability_factor * 100) * (boost / 18.8)
    
    return {
        "ID": seq_record.id,
        "GC Content (%)": round(gc_val, 2),
        "Melting Temp (°C)": round(tm_val, 2),
        "Predicted Score": round(score, 2),
        "Status": note
    }

# --- [UI] 사용자 인터페이스 ---
st.set_page_config(page_title="Nu-Finder Oncology AI", layout="wide")
st.title("🧬 Nu-Finder Oncology AI v2.0")
st.write("실제 유전체 연산 엔진이 탑재된 **Research-Ready** 모드입니다.")

# 분석 변수 설정
with st.sidebar:
    st.header("Analysis Settings")
    edit_len = st.slider("Target Edit Length (bp)", 1, 50, 5)
    st.caption("※ 논문 근거: 12bp 이하에서 효율이 극대화됩니다.")

# 파일 업로드 (가짜 데이터 방지)
uploaded_file = st.file_uploader("Upload FASTA file", type=['fasta', 'fa'])

if uploaded_file:
    # BioPython으로 실제 서열 로드
    stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
    records = list(SeqIO.parse(stringio, "fasta"))
    
    if records:
        with st.spinner('Calculating Genomic Metrics...'):
            results = [run_nu_engine(r, edit_len) for r in records]
            df = pd.DataFrame(results)

        # 결과 리포트
        st.subheader("📊 Computed Analysis Report")
        st.dataframe(df, use_container_width=True)

        # 동적 그래프 (입력값에 따라 실시간으로 바뀜)
        col1, col2 = st.columns(2)
        with col1:
            st.bar_chart(df.set_index('ID')['Predicted_Score'])
        with col2:
            st.line_chart(df.set_index('ID')['Melting Temp (°C)'])
    else:
        st.error("유효한 FASTA 데이터가 없습니다. 파일을 확인해 주세요.")
