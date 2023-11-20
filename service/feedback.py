import os
import openai
import time
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")
MODEL = "gpt-3.5-turbo"

start = time.time()  # 시작 시간

def get_feedback(question, answer, student_answer):
    USER_INPUT = f"문제: {question}, \n\n 모범 답안: {answer}, \n\n학생 답안: {student_answer}"
    USER_INPUT+= "\n\n 너는 선생님이고 채점을 하려고 해.\
            문제 수준에 맞는 학생에게 제공하는 말투로,\
            중요한 내용만 포함해서,\
            200자 이내로,\
            학생이 이해하기 쉽게, \
            문제와 모범답안을 기반으로 학생 답안에 대한 피드백만 제공해줘!"

    #chatGPT 답변
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": USER_INPUT},
        ],
        temperature=0,
    )

    feedback = response['choices'][0]['message']['content']
    print("time :", time.time() - start)  # 응답 시간
    return feedback