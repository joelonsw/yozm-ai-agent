from typing import Dict, Any
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field

class WorkflowStep:
    GREETING = "GREETING"
    PROCESSING = "PROCESSING"

class GraphState(BaseModel):
    name: str = Field(default="", description="사용자 이름")
    greeting: str = Field(default="", description="생성된 인사말")
    processed_message: str = Field(default="", description="처리된 최종 메시지")

# 첫 노드 함수 - greeting 부분만 GraphState에서 업데이트
def generate_greeting(state: GraphState) -> Dict[str, Any]:
    name = state.name or "아무개"
    greeting = f"안녕하세요, {name}님!"
    print("generate_greeting", greeting)
    return {"greeting": greeting}

# 두 번째 노드 함수 - processed_message 부분만 GraphState에서 업데이트
def process_message(state: GraphState) -> Dict[str, Any]:
    processed_message = state.greeting + " Langgraph welcomes you"
    print("process_message", processed_message)
    return {"processed_message": processed_message}

# 그래프 생성
def create_hello_graph():
    workflow = StateGraph(GraphState)

    # 노드 추가
    workflow.add_node(WorkflowStep.GREETING, generate_greeting)
    workflow.add_node(WorkflowStep.PROCESSING, process_message)

    # 시작 설정
    workflow.add_edge(START, WorkflowStep.GREETING)

    # 에지 추가
    workflow.add_edge(WorkflowStep.GREETING, WorkflowStep.PROCESSING)
    workflow.add_edge(WorkflowStep.PROCESSING, END)

    app = workflow.compile()

    return app

def main():
    print("Langgraph AI Agent")
    app = create_hello_graph()
    
    initial_state = GraphState(name="joel", greeting="hello", processed_message="...")
    print("init state: ", initial_state.model_dump())
    print("--- start graph ---")

    final_state = app.invoke(initial_state)

    print("--- end graph ---")
    print("final state: ", final_state)
    print("final message: ", {final_state['processed_message']})
    app.get_graph().draw_ascii()

if __name__ == "__main__":
    main()