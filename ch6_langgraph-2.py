from typing import Dict, Any, Literal
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import random
from dotenv import load_dotenv

load_dotenv()

class EmotionBotState(BaseModel):
    user_message: str = Field(default="", description="사용자 메시지")
    emotion: str = Field(default="", description="사용자 감정")
    response: str = Field(default="", description="최종 응답 메시지")

llm = ChatGroq(model = "openai/gpt-oss-120b")

def analyze_emotion(state: EmotionBotState) -> Dict[str, Any]:
    message = state.user_message
    print("LLM 감정 분석 중... ", message)
    messages = [
        SystemMessage(content="당신은 감정 분석 전문가입니다. 사용자 메시지를 분석하여 'positive', 'negative', 'neutral' 중 하나를 반환하세요."),
        HumanMessage(content=f"다음 메시지의 감정을 분석하세요: {message}")
    ]

    result = llm.invoke(messages)
    emotion = result.content.strip().lower()

    if emotion not in ["positive", "negative", "neutral"]:
        emotion = "neutral"
    
    print(f"LLM 감정 분석 결과 : {emotion}")
    return {"emotion": emotion}

def generate_positive_response(state: EmotionBotState) -> Dict[str, Any]:
    responses = ["정말 좋은 소식이네요!", "기분이 좋으시군요!", "멋지네요!"]
    return {"response": random.choice(responses)}

def generate_negative_response(state: EmotionBotState) -> Dict[str, Any]:
    responses = ["정말 안 좋은 소식이네요!", "기분이 안 좋으시군요!", "안 멋지네요!"]
    return {"response": random.choice(responses)}

def generate_neutral_response(state: EmotionBotState) -> Dict[str, Any]:
    responses = ["정말 그냥그런 소식이네요!", "기분이 그냥그런!", "그냥 그냥그런!"]
    return {"response": random.choice(responses)}

def route_by_emotion(state: EmotionBotState) -> Literal["positive_response", "negative_response", "neutral_response"]:
    print("route_by_emotion", state.emotion)
    return state.emotion + "_response"

def create_emotion_bot_graph():
    workflow = StateGraph(EmotionBotState)
    # 노드 추가
    workflow.add_node("analyze_emotion", analyze_emotion)
    workflow.add_node("positive_response", generate_positive_response)
    workflow.add_node("negative_response", generate_negative_response)
    workflow.add_node("neutral_response", generate_neutral_response)

    # 시작 설정
    workflow.add_edge(START, "analyze_emotion")

    # 조건부 에지 설정 - 동적 라우팅
    workflow.add_conditional_edges(
        "analyze_emotion",
        route_by_emotion,
        {
            "positive_response": "positive_response",
            "negative_response": "negative_response",
            "neutral_response": "neutral_response"
        }
    )

    workflow.add_edge("positive_response", END)
    workflow.add_edge("negative_response", END)
    workflow.add_edge("neutral_response", END)

    return workflow.compile()

def main():
    print("Langgraph 감정 분석")
    app = create_emotion_bot_graph()
    
    test_cases = [
        "오늘 기분 째지네~!",
        "아 진짜 빡친다",
        "날씨 어때요?"
    ]

    for test_case in test_cases:
        initial_state = EmotionBotState(user_message=test_case)
        print("--- start graph ---")
        final_state = app.invoke(initial_state)
        print("--- end graph ---")
        print("final state: ", final_state)
        print("final message: ", final_state['response'])

if __name__ == "__main__":
    main()
