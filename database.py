from sqlalchemy import create_engine, Column, String, Integer, JSON, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
import datetime

# 1. DB 설정 (PostgreSQL 연결 설정 - 실제 배포 시 환경변수 사용)
# DATABASE_URL = "postgresql://user:password@localhost/nufinder"
SQLALCHEMY_DATABASE_URL = "sqlite:///./nufinder_secure.db" # 로컬 테스트용

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. HIPAA 준수형 테이블 설계
class Patient(Base):
    __tablename__ = "patients"
    # PHI(개인식별정보)와 의료 데이터를 분리하기 위한 UUID
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    # 실제 이름/연락처는 암호화하여 저장해야 함 (Encrypted String)
    encrypted_name = Column(String, nullable=False) 
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class GenomicReport(Base):
    __tablename__ = "genomic_reports"
    id = Column(Integer, primary_key=True, index=True)
    patient_uuid = Column(String, ForeignKey("patients.id")) # Patient와 연결
    layer_1_data = Column(JSON)  # Bio-Logic 결과
    layer_2_data = Column(JSON)  # AI-Logic 결과
    layer_3_data = Column(JSON)  # Edit-Logic 결과
    full_sequence_hash = Column(String) # 원본 데이터 무결성 검증용
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(String) # 누가 접근했는가
    action = Column(String)  # 무엇을 했는가 (READ/WRITE)
    resource_id = Column(String) # 어떤 데이터에 접근했는가
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

# 3. FastAPI 엔드포인트에 DB 저장 로직 추가
# (기존 FastAPI 코드에 아래 저장 로직을 결합)
def save_analysis_result(patient_uuid, l1, l2, l3):
    db = SessionLocal()
    try:
        new_report = GenomicReport(
            patient_uuid=patient_uuid,
            layer_1_data=l1,
            layer_2_data=l2,
            layer_3_data=l3
        )
        db.add(new_report)
        
        # 감사 로그 남기기 (HIPAA 필수 사항)
        log = AuditLog(user_id="SYSTEM_ENGINE", action="CREATE_REPORT", resource_id=patient_uuid)
        db.add(log)
        
        db.commit()
    finally:
        db.close()
