import asyncio
from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate

from state import NewsState
from config import Config

class NewsSummarizerAgent:
    """뉴스 기사 요약 에이전트"""
    def __init__(self, llm: ChatGroq):
        self.name = "News Summarizer"
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",  # ② 시스템 역할 메시지로 AI의 행동 지침 설정
                    """당신은 전문 뉴스 요약 전문가입니다. 
                    주어진 뉴스를 핵심만 간결하게 2-3문장으로 요약해주세요.
                    - 사실만을 전달하고 추측은 피하세요
                    - 중요한 숫자나 날짜는 포함하세요
                    - 명확하고 이해하기 쉽게 작성하세요""",
                ),
                (
                    "human",  # ③ 사용자 메시지 템플릿에 변수 플레이스홀더 포함
                    "제목: {title}\n내용: {content}\n\n위 뉴스를 2-3문장으로 요약해주세요:",
                ),
            ]
        )
    
    async def summarize_single_news(self, news_item: Dict[str, Any]) -> Dict[str, Any]:
        """단일 뉴스 요약"""
        content = news_item.get("content", "")
        try:
            if not content or len(content) < 50:
                return {**news_item, "ai_summary": content}
            
            chain = self.prompt | self.llm
            summary_response = await chain.ainvoke(
                {
                    "title": news_item["title"],
                    "content": content[:500],
                }
            )
            summary = summary_response.content.strip()
            return {**news_item, "ai_summary": summary or content}
        except Exception as e:
            print(f"뉴스 요약 중 오류 발생: {e}")
            return {**news_item, "ai_summary": content}

    async def summarize_news(self, state: NewsState) -> NewsState:
        """뉴스 기사들을 요약합니다."""
        print("--- 뉴스 요약 시작 ---")
        batch_size = Config.BATCH_SIZE
        summarized_news = []
        raw_news = state.raw_news
        total_news = len(raw_news)

        for i in range(0, total_news, batch_size):
            batch = raw_news[i : i + batch_size]
            batch_num = i
            total_batches = total_news + batch_size - 1
            tasks = [self.summarize_single_news(news) for news in batch]
            batch_result = await asyncio.gather(*tasks)
            summarized_news.extend(batch_result)
    
        state.summarized_news = summarized_news
        state.messages.append(
            AIMessage(content=f"{len(summarized_news)}개의 뉴스 기사 요약 완료")
        )
        print(f"[{self.name}] 요약 완료 \n")
        return state