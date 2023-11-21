import torch

from sentence_transformers import util
from schema.grade_schema import GetGradeRequest


def predict_grade(request: GetGradeRequest):
    # 파인 튜닝 모델 불러오기
    device = torch.device('cpu')
    model = torch.load('./model/model.pt', map_location=device)
    model.eval()

    # 두 문장을 모델로 임베딩
    embeddings = model.encode([request.answer, request.student_answer], convert_to_tensor=True, device='cpu')

    # 코사인 유사도 계산
    return util.pytorch_cos_sim(embeddings[0], embeddings[1])[0][0].item()