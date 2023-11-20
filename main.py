from fastapi import FastAPI, HTTPException

from service.feedback import get_feedback
from service.grade import *

app = FastAPI()


"""
request 질문, 모범 답안, 학생 답안
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



"""
request 모범 답안, 학생 답안
response 채점 결과
"""
@app.post("/grade")
async def get_grade(request: GetGradeRequest):
    return predict_grade(request)