import streamlit as st
import pandas as pd
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction
import io
import math

# ===============================
# 1. Cancer Hotspot Knowledge Base
# ===============================
CANCER_HOTSPOTS = {
    "TP53": ["CGT", "GGC"],   # 대표적 missense hotspot 예시
    "KRAS": ["GGT"],          # codon 12
    "BRAF": ["TAC"]           # V600E (단순화)
}

# ===============================
# 2. Prime Editing Efficiency Model
# (논문 컨셉: GC 최적 = 50%, Gaussian decay)
# ===============================
def predict_pe_efficiency(gc):
    """
    Non-linear PE efficiency prediction
    """
    optimal_gc = 50
    sigma = 10  # 허용 폭
    efficiency = 90 * math.exp(-((gc - optimal_gc) ** 2) / (2 * sigma ** 2))
    return round(efficiency, 2)

# ===============================
# 3. Oncology Core Logic Engine
# ===============================
def analyze_oncology_logic(seq):
    # [A] GC content
    gc_val = gc_fraction(seq) * 100

    # [B] Hotspot-based mutation scan
    detected_genes = []
    for gene, motifs in CANCER_HOTSPOTS.items():
        for m in motifs:
            if m in seq:
                detected_genes.append(gene)
                break

    mutation_status = "Detected" if detected_genes else "Clean"

    # [C] Prime Editing efficiency prediction
    pe_eff = predict_pe_efficiency(gc_val)

    return {
        "GC_Content": round(gc_val, 2),
        "Mutation_Status": mutation_status,
        "Affected_Genes": ", ".join(detected_genes) if detected_genes else "-",
        "Predicted_PE_Efficiency": pe_eff
    }

# ===============================
# 4. Professional Visualization Layer
# ===============================
def display_professional_results(df):
    st.markdown("### 🧬 Nu-Finder Oncology Intelligence Report")

    results = []
    for _, row in df.iterrows():
        logic_res = analyze_oncology_logic(row["Full_Seq"])
        results.append(logic_res)

    res_df = pd.concat([df, pd.DataFrame(results)], axis=1)

    # --- Metrics Dashboard ---
    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Avg. PE Efficiency",
        f"{res_df['Predicted_PE_Efficiency'].mean():.1f}%",
        delta="Model-based"
    )
    col2.metric(
        "Mutation-Positive Targets",
        len(res_df[res_df["Mutation_Status"] == "Detected"])
    )
    col3.metric(
        "Avg. GC Content",
        f"{res_df['GC_Content'].mean():.1f}%"
    )

    st.divider()

    # --- Strategy Output ---
    st.subheader("🎯 Precision Editing Strategy")
    for _, row in res_df.iterrows():
        if row["Mutation_Status"] == "Detected":
            st.warning(
                f"**Target {row['ID']}** | "
                f"Affected Gene(s): {row['Affected_Genes']} | "
                f"Predicted PE Efficiency: **{row['Predicted_PE_Efficiency']}%**"
            )
            st.caption(
                "Recommendation: PE7 + SB2 적용, PAM 인접 pegRNA 설계 및 "
                "MMR suppression 고려"
            )
        else:
            st.success(
                f"**Target {row['ID']}**: Pathogenic hotspot 미검출"
            )

# ===============================
# 5. Streamlit UI
# ===============================
st.title("Nu-Finder Oncology AI")
st.caption("Precision Genome Editing Intelligence Engine")

file = st.file_uploader(
    "Upload Genomic Data (FASTA or CSV)",
    type=["fasta", "csv"]
)

if file:
    if file.name.endswith(".fasta"):
        stringio = io.StringIO(file.getvalue().decode("utf-8"))
        records = [
            {
                "ID": r.id,
                "Length": len(r.seq),
                "Full_Seq": str(r.seq)
            }
            for r in SeqIO.parse(stringio, "fasta")
        ]
        df = pd.DataFrame(records)

    elif file.name.endswith(".csv"):
        df = pd.read_csv(file)
        if "Full_Seq" not in df.columns or "ID" not in df.columns:
            st.error("CSV must contain 'ID' and 'Full_Seq' columns.")
            st.stop()

    display_professional_results(df)
