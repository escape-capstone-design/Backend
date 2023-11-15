from fastapi import FastAPI

from service.grade import *

app = FastAPI()


"""
request 모범 답안, 학생 답안
response 채점 결과
"""
@app.get("/grade")
async def get_grade(request: GetGradeRequest):
    return predict_grade(request)