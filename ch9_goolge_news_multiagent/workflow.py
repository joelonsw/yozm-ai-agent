from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from state import NewsState
from agents import (
    RSSCollectorAgent,
    NewsOrganizerAgent,
    ReportGeneratorAgent,
    NewsSummarizerAgent,
)

def create_news_workflow(llm: ChatGroq = None) -> StateGraph:
    """뉴스 처리 워크플로 생성 - RSS 수집 -> AI 요약 -> 카테고리 분류 -> 보고서 생성"""
    collector = RSSCollectorAgent()
    summarizer = NewsSummarizerAgent(llm)
    organizer = NewsOrganizerAgent(llm)
    reporter = ReportGeneratorAgent(llm)
    
    workflow = StateGraph(NewsState)

    workflow.add_node("collect", collector.collect_rss)
    workflow.add_node("summarize", summarizer.summarize_news)
    workflow.add_node("organize", organizer.organize_news)
    workflow.add_node("report", reporter.generate_report)

    workflow.set_entry_point("collect")

    workflow.add_edge("collect", "summarize")
    workflow.add_edge("summarize", "organize")
    workflow.add_edge("organize", "report")
    workflow.add_edge("report", END)

    return workflow.compile()