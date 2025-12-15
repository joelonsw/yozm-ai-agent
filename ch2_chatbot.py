from openai import OpenAI
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)

LITTLE_PRINCE_PERSONA = """
당신은 생텍쥐페리의 '어린 왕자'입니다. 다음 특성을 따라주세요:
1. 순수한 관점으로 세상을 바라봅니다.
2. "어째서?"라는 질문을 자주 하며 호기심이 많습니다.
3. 철학적 통찰을 단순하게 표현합니다.
4. "어른들은 참 이상해요"라는 표현을 씁니다.
5. B-612 소행성에서 왔으며 장미와의 관계를 언급합니다.
6. 여우의 "길들임"과 "책임"에 대한 교훈을 중요시합니다.
7. "중요한 것은 눈에 보이지 않아"라는 문장을 사용합니다.
8. 공손하고 친절한 말투를 사용합니다. 
9. 비유와 은유로 복잡한 개념을 설명합니다.

항상 간결하게 답변하세요. 길어야 2-3문장으로 응답하고, 어린 왕자의 순수함과 지혜를 담아내세요. 
복잡한 주제도 본질적으로 단순화하여 설명하세요.
"""

# 대화 기록을 저장할 리스트 (시스템 프롬프트로 초기화)
conversation_history = [
    {"role": "system", "content": LITTLE_PRINCE_PERSONA}
]

def get_ai_response(user_message: str, history: list):
    """
    대화 기록을 유지하면서 챗봇 응답을 생성합니다.
    """
    # 사용자 메시지를 대화 기록에 추가
    history.append({"role": "user", "content": user_message})
    
    # Groq Chat Completions API 호출
    result = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=history
    )
    
    # AI 응답 추출
    assistant_message = result.choices[0].message.content
    
    # AI 응답을 대화 기록에 추가
    history.append({"role": "assistant", "content": assistant_message})
    
    return assistant_message

def render_chat_page():
    """대화 기록을 HTML로 렌더링"""
    messages_html = ""
    for msg in conversation_history:
        if msg["role"] == "user":
            messages_html += f'<div class="message user"><strong>You:</strong> {msg["content"]}</div>'
        elif msg["role"] == "assistant":
            messages_html += f'<div class="message assistant"><strong>어린 왕자:</strong> {msg["content"]}</div>'
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>어린 왕자 챗봇</title>
        <meta charset="utf-8">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                padding: 20px;
            }}
            .container {{
                width: 100%;
                max-width: 700px;
            }}
            h1 {{
                color: #ffd700;
                text-align: center;
                margin-bottom: 20px;
                font-size: 2rem;
            }}
            .chat-box {{
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 16px;
                padding: 20px;
                height: 60vh;
                overflow-y: auto;
                margin-bottom: 20px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            .message {{
                padding: 12px 16px;
                margin: 10px 0;
                border-radius: 12px;
                line-height: 1.5;
            }}
            .user {{
                background: rgba(100, 150, 255, 0.3);
                color: #fff;
                margin-left: 20%;
            }}
            .assistant {{
                background: rgba(255, 215, 0, 0.2);
                color: #ffd700;
                margin-right: 20%;
            }}
            .loading {{
                background: rgba(255, 215, 0, 0.1);
                color: rgba(255, 215, 0, 0.6);
                margin-right: 20%;
                font-style: italic;
            }}
            form {{
                display: flex;
                gap: 10px;
            }}
            input[type="text"] {{
                flex: 1;
                padding: 15px 20px;
                border: none;
                border-radius: 25px;
                background: rgba(255, 255, 255, 0.15);
                color: #fff;
                font-size: 1rem;
                outline: none;
            }}
            input[type="text"]::placeholder {{
                color: rgba(255, 255, 255, 0.5);
            }}
            input:disabled {{
                opacity: 0.5;
            }}
            button {{
                padding: 15px 30px;
                border: none;
                border-radius: 25px;
                background: linear-gradient(135deg, #ffd700, #ff8c00);
                color: #1a1a2e;
                font-weight: bold;
                cursor: pointer;
                transition: transform 0.2s;
            }}
            button:hover {{
                transform: scale(1.05);
            }}
            button:disabled {{
                opacity: 0.5;
                cursor: not-allowed;
                transform: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌹 어린 왕자 챗봇</h1>
            <div class="chat-box" id="chatBox">
                {messages_html if messages_html else '<p id="placeholder" style="color: rgba(255,255,255,0.5); text-align: center;">어린 왕자에게 말을 걸어보세요...</p>'}
            </div>
            <form id="chatForm">
                <input type="text" id="userInput" name="user_message" placeholder="메시지를 입력하세요..." autofocus required>
                <button type="submit" id="sendBtn">전송</button>
            </form>
        </div>
        <script>
            const chatBox = document.getElementById('chatBox');
            const chatForm = document.getElementById('chatForm');
            const userInput = document.getElementById('userInput');
            const sendBtn = document.getElementById('sendBtn');
            
            function scrollToBottom() {{
                chatBox.scrollTop = chatBox.scrollHeight;
            }}
            
            function addMessage(role, content) {{
                // placeholder 제거
                const placeholder = document.getElementById('placeholder');
                if (placeholder) placeholder.remove();
                
                const div = document.createElement('div');
                div.className = 'message ' + role;
                if (role === 'user') {{
                    div.innerHTML = '<strong>You:</strong> ' + content;
                }} else if (role === 'assistant') {{
                    div.innerHTML = '<strong>어린 왕자:</strong> ' + content;
                }} else if (role === 'loading') {{
                    div.innerHTML = '<strong>어린 왕자:</strong> 생각 중...';
                    div.id = 'loadingMsg';
                }}
                chatBox.appendChild(div);
                scrollToBottom();
            }}
            
            chatForm.addEventListener('submit', async (e) => {{
                e.preventDefault();
                
                const message = userInput.value.trim();
                if (!message) return;
                
                // 즉시 사용자 메시지 표시
                addMessage('user', message);
                userInput.value = '';
                
                // 입력 비활성화
                userInput.disabled = true;
                sendBtn.disabled = true;
                
                // 로딩 메시지 표시
                addMessage('loading', '');
                
                try {{
                    // API 호출
                    const formData = new FormData();
                    formData.append('user_message', message);
                    
                    const response = await fetch('/chat', {{
                        method: 'POST',
                        body: formData
                    }});
                    
                    const data = await response.json();
                    
                    // 로딩 메시지 제거
                    const loadingMsg = document.getElementById('loadingMsg');
                    if (loadingMsg) loadingMsg.remove();
                    
                    // AI 응답 표시
                    addMessage('assistant', data.response);
                }} catch (error) {{
                    const loadingMsg = document.getElementById('loadingMsg');
                    if (loadingMsg) loadingMsg.remove();
                    addMessage('assistant', '오류가 발생했어요...');
                }}
                
                // 입력 다시 활성화
                userInput.disabled = false;
                sendBtn.disabled = false;
                userInput.focus();
            }});
            
            scrollToBottom();
        </script>
    </body>
    </html>
    """

@app.get("/", response_class=HTMLResponse)
async def home():
    """챗봇 UI 렌더링"""
    return render_chat_page()

@app.post("/chat")
async def chat(user_message: str = Form(...)):
    """사용자 입력 처리 후 AI 응답을 JSON으로 반환"""
    response = get_ai_response(user_message, conversation_history)
    return JSONResponse({"response": response})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
