from fastapi import FastAPI, HTTPException

from service.grade import *
from service.feedback import get_feedback

app = FastAPI()


"""
request 모범 답안, 학생 답안
response 채점 결과
"""
@app.get("/grade")
async def get_grade(request: GetGradeRequest):
    return predict_grade(request)


"""
request 문제, 모범 답안, 학생 답안
response 피드백 
"""
@app.post("/feedback")
async def feedback(data: dict):
    try:
        question = data.get("question")
        answer = data.get("answer")
        student_answer = data.get("student_answer")
        
        feedback = get_feedback(question, answer, student_answer)
        return {"feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
