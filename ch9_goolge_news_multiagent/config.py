import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """프로젝트 설정 관리 클래스"""
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    MODEL_NAME: str = "openai/gpt-oss-120b"
    MAX_TOKENS: int = 150
    ROOT_DIR: str = os.path.dirname(os.path.abspath(__file__))
    RSS_URL: str = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR+ko"
    MAX_NEWS_COUNT: int = 60
    BATCH_SIZE: int = 10
    NEWS_CATEGORIES: list[str] = [
        "정치", "경제", "사회", "생활", "스포츠", "연예", "기타"
    ]
    NEWS_PER_CATEGORY: int = 30
    OUTPUT_DIR: str = f"{ROOT_DIR}/outputs"

    # 설정의 유효성을 검사하는 클래스 메서드
    @classmethod
    def validate(cls) -> bool:
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set")
        return True