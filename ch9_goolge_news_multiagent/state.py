from typing import Annotated, Any
from pydantic import BaseModel, ConfigDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class NewsState(BaseModel):
    # pydantic이 모르는 타입을 허용
    model_config = ConfigDict(arbitrary_types_allowed=True)
    # 대화의 히스토리를 저장
    messages: Annotated[list[BaseMessage], add_messages] = []
    # RSS 피드에서 수집한 뉴스 데이터 저장
    raw_news: list[dict[str, Any]] = []
    # AI가 요약한 뉴스 데이터 저장
    summarized_news: list[dict[str, Any]] = []
    # 카테고리별 뉴스 저장
    categorized_news: dict[str, list[dict[str, Any]]] = {}
    # 리포트를 문자열로 저장
    final_report: str = ""
    # 에러 기록
    error_log: list[str] = []

