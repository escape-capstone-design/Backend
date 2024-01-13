from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from service.feedback import *
from service.grade import *
from core import models
from core.base import SessionLocal, engine

app = FastAPI()


#데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

#종속성 만들기 : 요청 당 독립적인 데이터베이스 세션/연결이 필요 요청이 완료되면 닫음
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""
request 모범 답안, 학생 답안
response 채점 결과
"""
@app.post("/grade")
async def get_grade(request: PredictGradeRequest):
    try:
        return predict_grade(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


"""
request 문제, 모범 답안, 학생 답안
response 피드백 
"""
@app.post("/feedback")
async def feedback(request: GetFeedbackRequest):
    try:
        feedback = get_feedback(request)
        return {"feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
