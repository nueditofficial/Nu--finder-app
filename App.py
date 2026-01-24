import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt  # <--- 이 줄이 167번 에러를 해결해줍니다!
import seaborn as sns

class TripleCheckEngine:
    def __init__(self, patient_data):
        self.data = patient_data
        self.risk_score = 0

    def analyze_snv(self, target_genes):
        """
        SNV(단일염기변이) 검출: 특정 위치의 염기 변화 확인
        예: G -> A 변이 탐지
        """
        # 실제 구현 시에는 BAM/VCF 파일을 로드하여 분석합니다.
        print("SNV 분석 중: 특정 변이 패턴 매칭...")
        # 임의의 로직: 특정 유전자 변이 발견 시 점수 부여
        snv_score = 25  # 가중치
        return snv_score

    def analyze_cnv(self):
        """
        CNV(유전자 복제수 변이) 분석: 유전자 증폭 패턴 감지
        """
        print("CNV 분석 중: 유전자 복제수 이상 확인...")
        cnv_score = 30
        return cnv_score

    def analyze_cfdna(self):
        """
        cfDNA 분석: 혈중 암 유래 DNA 농도 분석
        """
        print("cfDNA 분석 중: 미량 DNA 조각 패턴 분석...")
        cfdna_score = 45
        return cfdna_score

    def get_final_diagnosis(self):
        s = self.analyze_snv(['EGFR', 'TP53'])
        c = self.analyze_cnv()
        f = self.analyze_cfdna()
        self.risk_score = s + c + f
        return f"종합 위험도 점수: {self.risk_score}/100"

# 실행 예시
engine = TripleCheckEngine(patient_data="sample_001")
print(engine.get_final_diagnosis())
import json

# 1. 필터 설정: 폐암(LUAD) 환자의 유전자 변이 데이터(VCF/MAF) 찾기
filters = {
    "op": "and",
    "content": [
        {"op": "in", "content": {"field": "cases.project.project_id", "value": ["TCGA-LUAD"]}},
        {"op": "in", "content": {"field": "files.data_type", "value": ["Masked Somatic Mutation"]}},
        {"op": "in", "content": {"field": "files.data_format", "value": ["MAF"]}}
    ]
}

# 2. 파일 목록 요청
params = {
    "filters": json.dumps(filters),
    "fields": "file_id",
    "size": "5"  # 우선 샘플로 5개만 조회
}
response = requests.get("https://api.gdc.cancer.gov/files", params=params)
file_list = response.json()["data"]["hits"]

# 3. 실제 파일 다운로드 (첫 번째 파일 샘플)
if file_list:
    file_id = file_list[0]["file_id"]
    data_endpoint = f"https://api.gdc.cancer.gov/data/{file_id}"

    print(f"파일 다운로드 시작: {file_id}")
    file_response = requests.get(data_endpoint)

    with open("cancer_data_sample.maf.gz", "wb") as f:
        f.write(file_response.content)
    print("다운로드 완료! 'cancer_data_sample.maf.gz' 파일이 생성되었습니다.")
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. 데이터 로드 (가상의 유전자 변이 데이터셋)
# 실제로는 TCGA 등에서 수집한 CSV 파일을 불러옵니다.
data = {
    'gene_A_mutation': [1, 0, 1, 0, 1, 0, 0, 1],
    'gene_B_mutation': [0, 1, 1, 0, 0, 0, 1, 1],
    'cfDNA_level': [0.5, 0.1, 0.8, 0.2, 0.6, 0.1, 0.3, 0.7],
    'is_cancer': [1, 0, 1, 0, 1, 0, 0, 1]  # 정답지 (Label)
}
df = pd.DataFrame(data)

# 2. 데이터 분리 (학습용 vs 테스트용)
X = df.drop('is_cancer', axis=1)  # 특징 (Feature)
y = df['is_cancer']               # 타겟 (Target)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. AI 모델 생성 및 학습
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# 4. 예측 및 평가
predictions = model.predict(X_test)
print(f"모델 정확도: {accuracy_score(y_test, predictions) * 100}%")

# 5. 중요 변수 확인 (Triple Check의 핵심)
# 108번 줄 근처에 추가
mutation_matrix = X  # 기존에 정의된 X 데이터를 행렬 변수로 연결합니다.
importances = model.feature_importances_
for i, val in enumerate(importances):
    print(f"특징 {X.columns[i]}의 중요도: {val:.4f}")# 유전자별 변이 횟수 계산 및 상위 10개 출력
top_genes = mutation_matrix.sum().sort_values(ascending=False).head(10)
# 111번 줄 근처 수정
# 만약 앞에서 만든 학습 데이터 X가 변이 행렬이라면 아래와 같이 정의해줍니다.
mutation_matrix = X 

# 이제 top_genes를 계산합니다.
top_genes = mutation_matrix.sum().sort_values(ascending=False).head(10)

print("--- 가장 변이가 빈번한 유전자 Top 10 ---")
print(top_genes)

# 특정 유전자(예: EGFR)의 변이 여부 확인
target_gene = 'EGFR'
if target_gene in mutation_matrix.columns:
    count = mutation_matrix[target_gene].sum()
    print(f"\n{target_gene} 변이가 발견된 환자 수: {count}명")# 유전자별 변이 횟수 계산 및 상위 10개 출력
top_genes = mutation_matrix.sum().sort_values(ascending=False).head(10)

print("--- 가장 변이가 빈번한 유전자 Top 10 ---")
print(top_genes)

# 특정 유전자(예: EGFR)의 변이 여부 확인
target_gene = 'EGFR'
if target_gene in mutation_matrix.columns:
    count = mutation_matrix[target_gene].sum()
    print(f"\n{target_gene} 변이가 발견된 환자 수: {count}명")# 1. 환자별 정답 데이터(라벨) 로드 (가상의 예시)
# 실제로는 TCGA Clinical TSV 파일을 사용합니다.
clinical_data = {
    'Tumor_Sample_Barcode': mutation_matrix.index,
    'cancer_type': [1] * len(mutation_matrix) # 여기서는 모두 폐암(1)으로 가정
}
labels_df = pd.DataFrame(clinical_data).set_index('Tumor_Sample_Barcode')

# 2. 유전자 데이터와 정답 데이터 합치기
final_df = pd.concat([mutation_matrix, labels_df], axis=1)

# 3. AI 모델 학습 (간단한 예시)
from sklearn.ensemble import RandomForestClassifier

X = final_df.drop('cancer_type', axis=1) # 유전자 변이 정보 (문제)
y = final_df['cancer_type']              # 암 여부 (정답)

model = RandomForestClassifier()
model.fit(X, y)

print("\n--- AI 모델 학습 완료 ---")
print(f"학습에 사용된 유전자 수: {len(X.columns)}개")

import seaborn as sns

# 상위 15개 변이 유전자 추출
top_15_genes = mutation_matrix.sum().sort_values(ascending=False).head(15)

# 그래프 그리기
plt.figure(figsize=(12, 6))
sns.barplot(x=top_15_genes.values, y=top_15_genes.index, palette='viridis')
plt.title('Top 15 Mutated Genes in TCGA-LUAD', fontsize=15)
plt.xlabel('Number of Patients', fontsize=12)
plt.ylabel('Gene Symbol', fontsize=12)
plt.show()
# 상위 10개 유전자와 상위 50명 환자 샘플링
sample_matrix = mutation_matrix.iloc[:50, :10].T

plt.figure(figsize=(15, 8))
sns.heatmap(sample_matrix, cmap='YlGnBu', cbar=False, linewidths=.5)
plt.title('Genomic Mutation Heatmap (Patient vs Gene)', fontsize=15)
plt.xlabel('Patients', fontsize=12)
plt.ylabel('Genes', fontsize=12)
plt.show()


st.title("Nu-Finder Oncology AI")
st.write("유전자 데이터를 업로드하면 Triple Check 분석을 시작합니다.")

import streamlit as st
import pandas as pd
import time


# 2. 분석 결과 및 가이드를 보여주는 함수 (정의만 해둠)
def show_action_guide():
    st.markdown("---") 
    st.markdown("### 🚀 Nu-Solution Path")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💊 맞춤형 항암제 추천")
        drug_data = pd.DataFrame({
            '약물명': ['Pembrolizumab', 'Olaparib', 'Gefitinib'],
            '반응 가능성': [92, 45, 12]
        })
        st.bar_chart(drug_data.set_index('약물명'))

    with col2:
        st.subheader("✂️ NuEdit 편집 타겟")
        st.success("Target: Chromosome 17:41243452")
        st.code("Sequence: GATCG...TTAGC", language='text')

# 3. 파일 업로더 (이것도 딱 한 번만!)
uploaded_file = st.file_uploader("MAF 또는 CSV 파일 선택", type=['csv', 'maf'])

# 4. 파일이 올라왔을 때만 실행되는 로직
if uploaded_file is not None:
    with st.spinner('Nu-Logics AI가 유전체를 정밀 분석 중입니다...'):
        time.sleep(2) # 분석 시뮬레이션
    
    st.success("분석 완료!")
    
    # 여기서 결과 함수를 호출!
    show_action_guide()
from Bio import SeqIO # NCBI 서열 파일을 읽기 위한 도구
import io

# --- NCBI 파일 처리 함수 ---
def parse_ncbi_file(uploaded_file):
    # 업로드된 파일을 텍스트 형식으로 읽기
    stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
    
    # FASTA 형식을 리스트로 변환
    records = []
    for record in SeqIO.parse(stringio, "fasta"):
        records.append({
            "ID": record.id,
            "Description": record.description[:50] + "...",
            "Sequence_Length": len(record.seq),
            "Sequence_Snippet": str(record.seq[:20]) + "..."
        })
    return pd.DataFrame(records)

# --- 앱 메인 로직 수정 ---
uploaded_file = st.file_uploader("NCBI 데이터 업로드 (.fasta, .vcf)", type=['fasta', 'vcf', 'txt'])

if uploaded_file is not None:
    if uploaded_file.name.endswith('.fasta'):
        df = parse_ncbi_file(uploaded_file)
        st.write("🧬 NCBI 서열 분석 결과:")
        st.dataframe(df) # 화면에 깔끔한 표로 출력
        
        # 여기서 이제 우리의 show_action_guide()를 호출!
        show_action_guide()
