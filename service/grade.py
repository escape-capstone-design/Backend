import torch

from sentence_transformers import util
from schema.grade_schema import GetGradeRequest


def predict_grade(request: GetGradeRequest):
    # 파인 튜닝 모델 불러오기
    model = torch.load('./model/model.pt')
    model.eval()

    # 두 문장을 모델로 임베딩
    embeddings = model.encode([request.correct_answer, request.answer], convert_to_tensor=True)

    # 코사인 유사도 계산
    cosine_score = util.pytorch_cos_sim(embeddings[0], embeddings[1])
    return cosine_score