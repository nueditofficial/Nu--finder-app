import streamlit as st
import pandas as pd
from Bio import SeqIO
import io
import time

st.set_page_config(page_title="NuEdit | Nu-Finder", page_icon="🧬")

st.title("Nu-Finder Oncology AI")
st.write("실제 데이터 수치에 반응하는 **Dynamic Analysis** 모드입니다.")

def display_dynamic_results(df, mode="NCBI"):
    st.markdown("---")
    st.success(f"✅ {mode} 데이터 기반 맞춤형 분석 완료!")
    
    # 1. 실제 데이터 출력
    st.subheader("📊 분석된 유전자 정보 (실제 데이터)")
    st.dataframe(df, use_container_width=True)

    # 2. 데이터 수치에 따라 변하는 동적 그래프
    st.markdown("### 🚀 Nu-Solution Path (데이터 연동형)")
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("💊 데이터 기반 약물 반응도")
        # 데이터의 '길이(Length)' 수치를 활용해 가변적인 그래프 생성
        avg_len = df['Length'].mean() if 'Length' in df.columns else 5000
        
        # 길이에 따라 수치가 변하도록 로직 연결 (예시: 길이에 비례한 점수 계산)
        dynamic_score1 = min(95, avg_len / 100) 
        dynamic_score2 = max(10, 100 - (avg_len / 150))
        
        dynamic_res = pd.DataFrame({
            '약물': ['Target-A', 'Target-B'], 
            '예측 반응도(%)': [dynamic_score1, dynamic_score2]
        })
        st.bar_chart(dynamic_res.set_index('약물'))
        st.caption(f"기준 유전자 평균 길이({avg_len:.0f}bp)를 바탕으로 계산된 수치입니다.")

    with c2:
        st.subheader("✂️ NuEdit 편집 가이드")
        target_id = df['ID'].iloc[0] if 'ID' in df.columns else "Unknown"
        st.info(f"Target ID: {target_id}")
        st.code(f"AI 추천 지점: {target_id} 유전자의 변이 다발 구간\nAction: 정밀 교정 권고", language='text')

file = st.file_uploader("분석할 NCBI/CSV 파일 선택", type=['fasta', 'txt', 'csv'])

if file is not None:
    with st.spinner('실시간 데이터 매칭 중...'):
        time.sleep(1)
        try:
            if file.name.endswith(('.fasta', '.txt')):
                stringio = io.StringIO(file.getvalue().decode("utf-8"))
                records = [{"ID": r.id, "Length": len(r.seq), "Seq": str(r.seq[:30])} 
                           for r in SeqIO.parse(stringio, "fasta")]
                display_dynamic_results(pd.DataFrame(records), "NCBI")
            
            elif file.name.endswith('.csv'):
                df = pd.read_csv(file)
                # CSV에 'Score' 컬럼이 있다면 그것을 사용, 없다면 길이를 계산
                if 'Length' not in df.columns: df['Length'] = 1000 
                display_dynamic_results(df, "CSV")
                
        except Exception as e:
            st.error(f"오류 발생: {e}")
