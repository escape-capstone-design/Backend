from pydantic import BaseModel, field_validator


class GetGradeRequest(BaseModel):
    correct_answer: str
    answer: str

    @field_validator('correct_answer', 'answer')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v