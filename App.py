import streamlit as st
import pandas as pd
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction
import io

# 1. 핵심 설정 (불필요한 클래스/함수 래핑 제거)
HOTSPOTS = {"TP53": ["CGT", "GGC"], "KRAS": ["GGT"], "BRAF": ["TAC"]}

def get_efficiency(gc):
    """GC 50%에서 최적화되는 PE 효율 산출 (단순화된 수식)"""
    return round(90 * (2.718 ** -(((gc - 50) ** 2) / 200)), 2)

# 2. 메인 UI 및 로직
st.title("Nu-Finder: Genome Analyzer")

file = st.file_uploader("Upload FASTA or CSV", type=["fasta", "csv"])

if file:
    # 데이터 로드 (FASTA/CSV 통합 처리)
    if file.name.endswith(".fasta"):
        recs = SeqIO.parse(io.StringIO(file.getvalue().decode()), "fasta")
        df = pd.DataFrame([{"ID": r.id, "Seq": str(r.seq)} for r in recs])
    else:
        df = pd.read_csv(file)

    # 핵심 분석 (Pandas Vectorization 활용으로 속도 향상)
    df["GC"] = df["Seq"].apply(lambda x: gc_fraction(x) * 100)
    df["PE_Eff"] = df["GC"].apply(get_efficiency)
    
    # Gene 매칭 (복잡한 루프 대신 단순 포함 여부 확인)
    def detect_genes(seq):
        found = [gene for gene, motifs in HOTSPOTS.items() if any(m in seq for m in motifs)]
        return ", ".join(found) if found else "None"
    
    df["Genes"] = df["Seq"].apply(detect_genes)

    # 3. 결과 요약 및 출력
    cols = st.columns(3)
    cols[0].metric("Avg Efficiency", f"{df['PE_Eff'].mean():.1f}%")
    cols[1].metric("Targets Found", len(df[df["Genes"] != "None"]))
    cols[2].metric("Avg GC", f"{df['GC'].mean():.1f}%")

    st.dataframe(df[["ID", "GC", "Genes", "PE_Eff"]], use_container_width=True)

    # 탐지된 타겟만 간결하게 표시
    hits = df[df["Genes"] != "None"]
    if not hits.empty:
        st.subheader("🎯 Actionable Targets")
        for _, r in hits.iterrows():
            st.error(f"**{r['ID']}** ({r['Genes']}): {r['PE_Eff']}% efficiency. Need MMR suppression.")
