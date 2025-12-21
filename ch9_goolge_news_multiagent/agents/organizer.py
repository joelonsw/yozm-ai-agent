import asyncio
from collections import defaultdict
from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from state import NewsState
from config import Config


class NewsOrganizerAgent:
    """뉴스 기사들을 주제별로 정리하는 에이전트"""
    def __init__(self, llm: ChatGroq):
        self.name = "News Organizer"
        self.llm = llm
        self.categories = Config.NEWS_CATEGORIES
        system_prompt = f"""당신은 전문 뉴스 정리 전문가입니다. 주어진 뉴스를 주제별로 정리해주세요. {", ".join(Config.NEWS_CATEGORIES)}. 반드시 위 카테고리 중 하나만 선택하고, 카테고리 값만 반환하세요."""

        self.categorize_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "제목: {title}\n요약: {summary}\n\n위 뉴스의 카테고리:"),
            ]
        )
        self.chain = self.categorize_prompt | self.llm
    
    async def categorize_single_news(self, news_item: Dict[str, Any]) -> tuple[str, Dict[str, Any]]:
        """단일 뉴스를 주제별로 정리"""
        response = await self.chain.ainvoke(
            {
                "title": news_item["title"],
                "summary": news_item.get("ai_summary", news_item["content"])
            }
        )
        category = response.content.strip()
        return category, news_item
    
    async def organize_news(self, state: NewsState) -> NewsState:
        """뉴스 기사들을 주제별로 정리합니다."""
        print("--- 뉴스 정리 시작 ---")
        summarized_news = state.summarized_news
        batch_size = Config.BATCH_SIZE
        total_news = len(summarized_news)
        categorized = defaultdict(list)

        for i in range(0, total_news, batch_size):
            batch = summarized_news[i : i + batch_size]
            batch_num = i
            total_batches = total_news + batch_size - 1
            print(f"[{self.name}] {batch_num + 1}/{total_batches} 배치 처리 중...")

            tasks = [self.categorize_single_news(news) for news in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, Exception):
                    print(f"뉴스 정리 중 오류 발생: {result}")
                    continue
                else:
                    category, news_item = result
                    if category in Config.NEWS_CATEGORIES:
                        categorized[category].append(news_item)
                    else:
                        categorized["기타"].append(news_item)
        
        print("\n 카테고리별 분포")
        for category, news in categorized.items():
            print(f"{category}: {len(news)}")
        
        state.categorized_news = dict(categorized)
        state.messages.append(
            AIMessage(content=f"{len(categorized)}개의 카테고리로 분류했습니다")
        )
        print(f"[{self.name}] 정리 완료 \n")
        return state