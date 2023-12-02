import torch
from enum import Enum

from sentence_transformers import util
from schema.grade_schema import GetGradeRequest


# 채점 결과
class TestResult(Enum):
    CORRECT = "정답 :)"
    NEEDS_CONFIRMATION = "해당 문항에 대한 정답 여부를 확인하기 어려워, 추가적인 확인이 필요합니다. 피드백을 참고하여 답안을 다시 작성해보세요 :) "
    WRONG = "오답 :("


def predict_grade(request: GetGradeRequest):
    # 파인 튜닝 모델 불러오기
    device = torch.device('cpu')
    model = torch.load('./model/model.pt', map_location=device)
    model.eval()

    # 두 문장을 모델로 임베딩
    embeddings = model.encode([request.answer, request.student_answer], convert_to_tensor=True, device='cpu')

    # 코사인 유사도 계산
    cosine_similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1])[0][0].item()

    if cosine_similarity >= 0.7:
        result = TestResult.CORRECT.value
    elif cosine_similarity <= 0.5:
        result = TestResult.WRONG.value
    else:
        result = TestResult.NEEDS_CONFIRMATION.value

    return '\n'.join([str(result), str(cosine_similarity)])