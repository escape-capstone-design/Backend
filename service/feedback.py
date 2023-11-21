import os
import openai
import time
from dotenv import load_dotenv
from schema.feedback_schema import GetFeedbackRequest
# .env 파일 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")
MODEL = "gpt-3.5-turbo"


def get_feedback(request :GetFeedbackRequest):
    
    USER_INPUT = f"문제: {request.question}, \n\n 모범 답안: {request.answer}, \n\n학생 답안: {request.student_answer}"
    USER_INPUT+= "\n\n 너는 선생님이고 채점을 하려고 해.\
            문제 수준에 맞는 학생에게 제공하는 말투로,\
            중요한 내용만 포함해서,\
            200자 이내로,\
            학생이 이해하기 쉽게, \
            문제와 모범답안을 기반으로 학생 답안에 대한 피드백만 제공해줘!"

    #시작 시간 기록
    start_time = time.time()  
    
    #chatGPT에게 피드백 요청
    feedback = get_gpt_response(USER_INPUT)

    #피드백 검증
    #검증 시 "아니오"를 출력하였다면, 다른 피드백을 제공하도록 함
    while not verify_feedback(USER_INPUT, feedback):
        
        # 1분 넘으면 무한루프 종료
        elapsed_time = time.time() - start_time
        if elapsed_time > 60:  
            print("Timeout: Exiting the loop.")
            break
        
        again = "다른 피드백을 다시 제공해줘."
        feedback = get_gpt_response_multiple_inputs(request.question, request.answer, again)
        
    return feedback


#피드백 검증
def verify_feedback(question, feedback):
    USER_INPUT = "모범답안과 학생답안을 비교했을 때, 적절한 피드백이야? 단답으로 네,아니오 둘 중 하나로 대답해줘"
    response = get_gpt_response_multiple_inputs(question,feedback, USER_INPUT)
    print(response)
    if response and response.startswith('네'):
        return True
    else:
        return False
    
    
    
def get_gpt_response(input):
        response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": input},
        ],
        temperature=0,
        )
        return response['choices'][0]['message']['content']


#문제,모범답안,학생답안,제공한 피드백 내용을 기억하게 한 후 새로운 질문
def get_gpt_response_multiple_inputs(question, feedback, input):
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": question},
            {"role": "assistant", "content": feedback},
            {"role": "user", "content": input},
        ],
        temperature=0,
    )
    return response['choices'][0]['message']['content']