from typing import Literal
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class AgentState(BaseModel):
    user_message: str = Field(default="", description="user_message")
    task_details: str = Field(default="", description="task_details")
    response: str = Field(default="", description="response")

def get_llm_response_node(state: AgentState, llm):
    details = state.task_details
    
    if details:
        print(f"\n상세 정보를 바탕으로 작업 실행: '{details}'")
        prompt = f"주제: {state.user_message}\n요구사항: {details}\n\n위 주제와 요구사항에 맞춰 보고서를 작성해주세요. 완성된 보고서 전문을 출력하세요."
    else:
        task = state.user_message
        print(f"\n작업 실행: '{task}' 작업을 수행합니다 .")
        prompt = f"'{task}' 작업을 수행하려고 합니다. 어떤 종류의 보고서가 필요한지, 구체적인 주제는 무엇인지 질문해주세요. 추가정보가 필요하면, 반드시 응답의 마지막을 물음표('?')로 끝내주세요."

    response = llm.invoke(prompt).content

    print(response)
    return {"response": response, "task_details": ""}

def get_task_details_node(state: AgentState) -> AgentState:
    print("\nLLM의 질문에 답변해주세요.")
    user_input = input("답변: ")
    return {"task_details": user_input}

def check_llm_response(state: AgentState) -> Literal["get_details", "end"]:
    print("LLM 응답 분석 중")
    if state.response.endswith("?"):
        print("LLM 추가 정보 요청했습니다. 사용자 입력 받습니다.")
        return "get_details"
    print("최종 보고서가 생성되었습니다. 작업 종료")
    return "end"

def create_graph():
    """Human-in-the-loop(Agent)"""
    llm = ChatGroq(model = "openai/gpt-oss-120b")

    def get_llm_response_with_llm(state):
        return get_llm_response_node(state, llm)

    workflow = StateGraph(AgentState)
    workflow.add_node("get_llm_response", get_llm_response_with_llm)
    workflow.add_node("get_details", get_task_details_node)

    workflow.add_edge(START, "get_llm_response")
    workflow.add_conditional_edges(
        "get_llm_response",
        check_llm_response,
        {
            "get_details": "get_details",
            "end": END
        }
    )    
    
    workflow.add_edge("get_details", "get_llm_response")
    return workflow.compile()

def main():
    print("Langgraph Human-in-the-loop(Agent)")
    app = create_graph()
    
    user_input = input("주제를 입력하세요: ")
    final_state = app.invoke(AgentState(user_message=user_input))
    print("final state: ", final_state)
    print("final message: ", final_state['response'])

if __name__ == "__main__":
    main()
    