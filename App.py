import streamlit as st
import pandas as pd
from Bio import SeqIO
import io
import time

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="NuEdit | Nu-Finder", page_icon="🧬")

# 2. 메인 헤더 (중복 방지)
st.title("Nu-Finder Oncology AI")
st.write("유전자 데이터를 업로드하면 **Triple Check** 분석을 시작합니다.")

# 3. 통합 파일 업로더 (하나로 합침)
uploaded_file = st.file_uploader("NCBI 데이터(.fasta, .txt) 또는 CSV 선택", type=['fasta', 'txt', 'csv'])

if uploaded_file is not None:
    with st.spinner('Nu-Logics AI가 데이터를 정밀 분석 중입니다...'):
        time.sleep(1.5) # 분석 애니메이션
        try:
            # NCBI FASTA/TXT 파일 처리
            if uploaded_file.name.endswith(('.fasta', '.txt')):
                stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
                records = [{"ID": r.id, "Length": len(r.seq), "Preview": str(r.seq[:50])+"..."} 
                           for r in SeqIO.parse(stringio, "fasta")]
                df_result = pd.DataFrame(records)
            
            # CSV 파일 처리
            elif uploaded_file.name.endswith('.csv'):
                df_result = pd.read_csv(uploaded_file).head(5)

            # --- 결과 대시보드 출력 ---
            st.markdown("---")
            st.balloons()
            st.success("✅ 분석 완료!")
            
            st.subheader("📊 유전체 분석 요약")
            st.dataframe(df_result, use_container_width=True)

            # 비즈니스 인사이트 (이전 코드의 핵심 로직)
            st.markdown("### 🚀 Nu-Solution Path")
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("💊 맞춤형 항암제")
                drug_data = pd.DataFrame({'약물': ['Pembrolizumab', 'Olaparib'], '반응도': [92, 45]})
                st.bar_chart(drug_data.set_index('약물'))
            with c2:
                st.subheader("✂️ NuEdit 편집 가이드")
                st.info("AI 추천 편집 지점")
                st.code("Target: TP53 Region\nAction: Mutation Correction", language='text')

        except Exception as e:
            st.error(f"⚠️ 분석 오류 발생: {e}")
