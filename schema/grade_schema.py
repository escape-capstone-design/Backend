from pydantic import BaseModel, field_validator


class PredictGradeRequest(BaseModel):
    answer: str
    student_answer: str

    @field_validator('answer', 'student_answer')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class PredictGradeResponse(BaseModel):
    result: str
    score: float
