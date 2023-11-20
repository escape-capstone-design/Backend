from fastapi import FastAPI,HTTPException

from service.feedback import get_feedback
from service.grade import *

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


#feedback 요청
@app.post("/feedback")
async def feedback(data: dict):
    try:
        #임시
        #question = "태양 에너지와 광합성이 지구의 기후 및 환경에 어떤 영향을 미치는지에 대해 설명하십시오."
        #answer = "태양으로부터 오는 에너지는 식물들에 의해 광합성에 사용되며, 이것은 지면의 열을 증가시키고 대기온도와 함께 바람 및 물 변화량과 연결된다."
        #tudent_answer = "태양 에너지는 지구의 기온을 낮추고 대기의 기온을 하락시키며, 식물의 광합성에 영향을 주지 않습니다."
        
        #실제 front에서 넘어오는 question, answer, student_answer
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
@app.get("/grade")
async def get_grade(request: GetGradeRequest):
    return predict_grade(request)