from pydantic import BaseModel


class GetGradeRequest(BaseModel):
    answer: str
    student_answer: str