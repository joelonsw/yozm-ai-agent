import random
from langchain.tools import tool
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

@tool
def rps() -> str:
    """Play rock paper scissors - returns a random choice of rock, paper, or scissors."""
    return random.choice(["rock", "paper", "scissors"])

llm = ChatGroq(model="openai/gpt-oss-20b").bind_tools([rps])
llm_for_chat = ChatGroq(model="openai/gpt-oss-20b")
print(type(llm))

def judge(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "draw"
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "paper" and computer_choice == "rock") or \
         (user_choice == "scissors" and computer_choice == "paper"):
        return "user"
    else:
        return "computer"

print("Let's play Rock Paper Scissors! (quit : q)")
while (user_input := input("rps: ")) != "q":
    ai_msg = llm.invoke("Play Rock Paper Scissors! user's choice: " + user_input)
    print(ai_msg)

    if ai_msg.tool_calls:
        print(type(rps))
        llm_choice = rps.invoke("")
        print(f" LLM 선택한 도구: {llm_choice}")
        result = judge(user_input, llm_choice)
        print(f"Result: {result}")

        final = llm_for_chat.invoke(
            f"가위바위보 해설해줘요"
            f"사용자: {user_input}"
            f"AI: {llm_choice}"
            f"결과: {result}"
        )
        print(f" LLM 해설: {final.content}")