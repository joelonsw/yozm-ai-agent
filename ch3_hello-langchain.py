from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
import random
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.messages import AIMessage
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

load_dotenv()

# https://docs.langchain.com/oss/python/integrations/chat

# if random.random() < 0.5:
#     print("openai/gpt-oss-20b selected")
#     model = init_chat_model(
#         model="openai/gpt-oss-20b",
#         model_provider="openai",
#         api_key=os.environ.get("GROQ_API_KEY"),     # 직접 전달
#         base_url="https://api.groq.com/openai/v1"   # 직접 전달
#     )
# else:
#     print("groq/compound selected")
#     model = init_chat_model(
#         model="groq/compound",
#         model_provider="groq"
#     )

# result = model.invoke("랭체인이 뭔가요? 30자 이내로 설명")
# print(type(result))
# print(result.content)

chat_model = ChatGroq(model = "openai/gpt-oss-20b")

# LLM이 뱉는 여러 미사여구를 JSON으로 깔끔하게 정제
json_output_parser = JsonOutputParser()

chat_prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful NHL analyst. \n{format_instructions}"),
    ("human", "{question}")
])

chain = chat_prompt_template | chat_model | json_output_parser

# RunnableSequence : 실행, 배치, 스트리밍에 대한 담당
print(type(chain))

parsed_result = chain.invoke({
    "question": "Name the top 5 NHL players of all time with their team.",
    "format_instructions": json_output_parser.get_format_instructions()
})

print(parsed_result)
