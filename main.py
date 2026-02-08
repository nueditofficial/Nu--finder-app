from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import math

app = FastAPI(title="Nu-Finder Oncology Engine")

# 프론트엔드(Streamlit)와 통신을 위한 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터 모델 정의
class SequenceRequest(BaseModel):
    sequence: str
    patient_id: str

# --- ENGINE LAYERS ---

def layer_1_bio_logic(seq):
    """변이 식별 및 공공 DB 매칭 (결정론적 알고리즘)"""
    hotspots = {"GGT": "KRAS (Codon 12)", "CGT": "TP53 (R175H)", "TAC": "BRAF (V600E)"}
    detected = [gene for motif, gene in hotspots.items() if motif in seq.upper()]
    return detected if detected else ["None"]

def layer_2_ai_logic(detected_genes):
    """예후 및 약물 반응성 예측 (가중치 모델)"""
    if "None" in detected_genes:
        return {"prognosis_score": 95, "drug_response": "Standard Care"}
    # 변이가 있을 경우 예후 점수 하락 및 특정 약물 추천
    return {"prognosis_score": 45, "drug_response": "Targeted Therapy (Sotorasib/Vemurafenib)"}

def layer_3_edit_logic(seq):
    """Prime Editing 효율 및 오프타겟 시뮬레이션"""
    # GC 함량 기반 효율 계산 (논문 근거 Gaussian 모델)
    gc_content = (seq.upper().count('G') + seq.upper().count('C')) / len(seq) * 100
    efficiency = 90 * math.exp(-((gc_content - 50) ** 2) / 200)
    
    # 가상의 오프타겟 시뮬레이션 (서열 복잡도 기준)
    off_target_risk = "Low" if len(set(seq)) > 3 else "High"
    
    return {
        "pe_efficiency": round(efficiency, 2),
        "off_target_risk": off_target_risk,
        "recommended_pegRNA": "v4.2_Optimized"
    }

# --- API ENDPOINT ---

@app.post("/analyze")
async def analyze_genomics(request: SequenceRequest):
    try:
        # Layer 1: Bio
        genes = layer_1_bio_logic(request.sequence)
        
        # Layer 2: AI
        prognosis = layer_2_ai_logic(genes)
        
        # Layer 3: Edit
        editing = layer_3_edit_logic(request.sequence)
        
        return {
            "patient_id": request.patient_id,
            "layer_1_bio": {"detected_genes": genes},
            "layer_2_ai": prognosis,
            "layer_3_edit": editing,
            "status": "Success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
