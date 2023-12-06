from fastapi import FastAPI, HTTPException

from service.feedback import *
from service.grade import *

app = FastAPI()


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