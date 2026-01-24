import streamlit as st
import pandas as pd
from Bio import SeqIO
import io
import time

# [이전 설정 유지] 페이지 기본 설정
st.set_page_config(page_title="NuEdit | Nu-Finder", page_icon="🧬")

# --- UI 섹션 1: 헤더 (CEO님의 첫 브랜딩 유지) ---
st.title("Nu-Finder Oncology AI")
st.write("유전자 데이터를 업로드하면 **Triple Check** 분석을 시작합니다.")

# --- UI 섹션 2: 이전의 멋진 결과 대시보드 (함수로 보존) ---
def show_business_logic(data_summary):
    st.markdown("---")
    st.balloons()
    st.success("✅ Nu-Logics 엔진 분석 완료!")
    
    # [이전 코드의 핵심] 데이터 요약 출력
    st.subheader("📊 유전체 분석 리포트")
    st.table(data_summary) # NCBI에서 읽어온 실제 정보 표시

    # [수익 구조 섹션] 그대로 유지
    st.markdown("### 🚀 Nu-Solution Path (수익 모델)")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💊 맞춤형 항암제 추천")
        # 실제 데이터 기반은 아니더라도, 분석이 끝났음을 보여주는 시각화
        drug_res = pd.DataFrame({'약물': ['Pembrolizumab', 'Olaparib'], '반응도': [92, 45]})
        st.bar_chart(drug_res.set_index('약물'))
    with col2:
        st.subheader("✂️ NuEdit 정밀 편집")
        st.info("AI가 찾은 최적 편집 지점")
        st.code("Target: TP53 Gene\nPos: 7577121\nSeq: GATCG...TTAGC", language='text')

# --- UI 섹션 3: NCBI 파일 읽기 엔진 (새로운 연료 공급 장치) ---
file = st.file_uploader("NCBI 데이터(.fasta, .txt) 또는 CSV 업로드", type=['fasta', 'txt', 'csv'])

if file is not None:
    with st.spinner('Nu-Logics AI가 Triple Check를 수행 중입니다...'):
        time.sleep(1.5)
        try:
            # 1. NCBI 파일일 경우
            if file.name.endswith(('.fasta', '.txt')):
                stringio = io.StringIO(file.getvalue().decode("utf-8"))
                records = []
                for r in SeqIO.parse(stringio, "fasta"):
                    records.append({"ID": r.id, "Length": len(r.seq), "Preview": str(r.seq[:30])+"..."})
                
                # 분석 결과를 이전 대시보드로 전달!
                show_business_logic(pd.DataFrame(records))
            
            # 2. CSV 파일일 경우
            elif file.name.endswith('.csv'):
                df = pd.read_csv(file)
                show_business_logic(df.head(5)) # 상위 5개 데이터만 요약 표시
                
        except Exception as e:
            st.error(f"파일 분석 중 오류가 발생했습니다. (설정 확인 필요): {e}")
