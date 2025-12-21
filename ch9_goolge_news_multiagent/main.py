import os
import logging
import asyncio
from datetime import datetime
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from workflow import create_news_workflow
from state import NewsState
from config import Config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger(__name__)

async def main():
    """뉴스 처리 워크플로를 실행합니다."""
    logger.info("뉴스 처리 워크플로 시작")
    
    try:
        if not Config.validate():
            raise ValueError("Invalid configuration")
        
        llm = ChatGroq(
            model_name=Config.MODEL_NAME,
            max_tokens=Config.MAX_TOKENS,
            api_key=Config.GROQ_API_KEY,
        )
        workflow = create_news_workflow(llm)
        
        initial_state = NewsState(
            messages=[HumanMessage(content="Google News RSS 처리 시작!")]
        )
        final_state = await workflow.ainvoke(initial_state)

        if not final_state.get("final_report"):
            print("\n생성된 보고서가 없습니다")
            return

        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(Config.OUTPUT_DIR, f"news_report_{timestamp}.md")

        with open(filename, "w", encoding="utf-8") as f:
            f.write(final_state["final_report"])

        print("\n" + "=" * 60)
        print("처리 완료")
        print("=" * 60)
        print(f"\n보고서가 저장되었습니다: {filename}")
        print(f"처리된 뉴스: {len(final_state.get('summarized_news', []))}건")
        print("\n보고서 미리보기:")
        print("-" * 60)
        print(final_state["final_report"][:500] + "...")

    # ⑥ 예외 처리 - 사용자 중단과 일반 오류를 구분하여 처리
    except KeyboardInterrupt:
        print("\n\n사용자에 의해 중단되었습니다.")
    except Exception as e:
        logger.exception("실행 중 오류 발생")
        print(f"\n오류 발생: {e}")


# ⑦ 프로그램 진입점 - 비동기 메인 함수를 실행
if __name__ == "__main__":
    asyncio.run(main())