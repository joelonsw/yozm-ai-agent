import os
import rich
import asyncio

from dotenv import load_dotenv
from openai import OpenAI
from openai import AsyncOpenAI

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)

async_client = AsyncOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)

async def call_async_client(prompt):
    response = await async_client.responses.create(
        model="openai/gpt-oss-20b",
        input=prompt,
    )
    return response.output_text

def get_response(prompt, model = "openai/gpt-oss-20b"):
    response = client.responses.create(
        model=model,
        input=prompt,
        tools=[
            {
                "type": "browser_search"
            }
        ],
    )
    return response.output_text

def stream_response(prompt, model = "openai/gpt-oss-20b"):
    with client.responses.stream(model=model, input=prompt) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                print(event.delta, end="", flush=True)
            elif event.type == "response.output_text.done":
                print()

async def main():
    async_task_1 = call_async_client("아시아리그 아이스하키에 대해 알려주세요.")
    async_task_2 = call_async_client("HL안양에 대해 알려주세요.")
    async_response_1, async_response_2 = await asyncio.gather(async_task_1, async_task_2)
    print(async_response_1)
    print(async_response_2)

if __name__ == "__main__":
#     prompt = """
# https://namu.wiki/w/%EC%95%84%EC%8B%9C%EC%95%84%EB%A6%AC%EA%B7%B8%20%EC%95%84%EC%9D%B4%EC%8A%A4%ED%95%98%ED%82%A4
# 를 읽어서 아시아리그 아이스하키에 대해 요약 정리해주세요. 
# """
#     output = get_response(prompt)
#     print(output)
#     stream_response("NHL 대해 요약 정리하여 알려주세요.")

    asyncio.run(main())