# 🤖 AI 에이전트 실습

> 📚 **[요즘 AI 에이전트 개발](https://product.kyobobook.co.kr/detail/S000217241525)** 책을 기반으로 실습하는 프로젝트입니다.

## 📁 프로젝트 구조

```
alih-agent/
├── ch1_hello-ai.py    # Chapter 1: AI 첫 만남
├── ch2_chatbot.py     # Chapter 2: 챗봇 (어린 왕자 페르소나)
├── .env               # 환경 변수 (API 키)
└── .gitignore
```

## 🚀 시작하기

### 1. 가상환경 설정
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2. 의존성 설치
```bash
pip install openai python-dotenv fastapi uvicorn python-multipart
```

### 3. 환경 변수 설정
`.env` 파일을 생성하고 API 키를 추가하세요:
```
GROQ_API_KEY=your_api_key_here
```

### 4. 실행
```bash
# Chapter 2: 어린 왕자 챗봇 (웹 UI)
python ch2_chatbot.py
# http://localhost:8000 에서 확인
```

## 📖 실습 내용

| 챕터 | 내용 | 파일 |
|------|------|------|
| Ch1 | AI API 기본 사용법 | `ch1_hello-ai.py` |
| Ch2 | 대화 기억 챗봇 + FastAPI 웹 UI | `ch2_chatbot.py` |

---

✨ Made with 💜 while reading **요즘 AI 에이전트 개발**
