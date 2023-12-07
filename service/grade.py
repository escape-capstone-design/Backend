import torch
from enum import Enum

from sentence_transformers import util,models,SentenceTransformer
from schema.grade_schema import PredictGradeRequest, PredictGradeResponse


# 채점 결과
class TestResult(Enum):
    CORRECT = "정답 :)"
    NEEDS_CONFIRMATION = "해당 문항에 대한 정답 여부를 확인하기 어려워, 추가적인 확인이 필요합니다. 피드백을 참고하여 답안을 다시 작성해보세요 :) "
    WRONG = "오답 :("


def predict_grade(request: PredictGradeRequest):
    
    #모델 불러오기
    embedding_model = models.Transformer(
        model_name_or_path="BM-K/KoSimCSE-roberta-multitask",
        max_seq_length=150,
        do_lower_case=True
    )

    pooling_model = models.Pooling(
        embedding_model.get_word_embedding_dimension(),
        pooling_mode_mean_tokens=True,
        pooling_mode_cls_token=False,
        pooling_mode_max_tokens=False,
    )
    model = SentenceTransformer(modules=[embedding_model, pooling_model])
    
    #파인튜닝 state_dict 불러오기
    device = torch.device('cpu')
    model.load_state_dict(torch.load('./model/model_state_dict.pt',map_location=device),strict=False)
    model.eval()

    # 두 문장을 모델로 임베딩
    embeddings = model.encode([request.answer, request.student_answer], convert_to_tensor=True, device='cpu')

    # 코사인 유사도 계산
    cosine_similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1])[0][0].item()
    score = round(cosine_similarity, 2) * 100

    if cosine_similarity >= 0.7:
        result = TestResult.CORRECT.value
    elif cosine_similarity <= 0.5:
        result = TestResult.WRONG.value
    else:
        result = TestResult.NEEDS_CONFIRMATION.value

    return PredictGradeResponse(result=result, score=score)
