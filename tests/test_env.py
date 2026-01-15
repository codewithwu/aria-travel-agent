import os
from dotenv import load_dotenv

load_dotenv()

print("环境变量测试:")
print(f"LLM_PROVIDER: {os.getenv('LLM_PROVIDER')}")
print(f"Ollama_BaseUrl 是否存在: {'是' if os.getenv('Ollama_BaseUrl') else '否'}")
print(f"Ollama_MODEL_NAME 是否存在: {'是' if os.getenv('Ollama_MODEL_NAME') else '否'}")

# # 测试OpenAI客户端（可选）
# try:
#     from openai import OpenAI
#     client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
#     print("✓ OpenAI客户端初始化成功")
# except Exception as e:
#     print(f"✗ OpenAI客户端初始化失败: {e}")

# # 测试Groq客户端（可选）
# try:
#     from groq import Groq
#     client = Groq(api_key=os.getenv('GROQ_API_KEY'))
#     print("✓ Groq客户端初始化成功")
# except Exception as e:
#     print(f"✗ Groq客户端初始化失败: {e}")


# 测试Groq客户端（可选）
try:
    from langchain_ollama import ChatOllama
    model = ChatOllama(
            model="gpt-oss:20b",
            base_url=os.getenv('Ollama_BaseUrl'),
            validate_model_on_init=True,
            temperature=0.8,
            num_predict=256,
        )
    print("✓ 本地Ollama客户端初始化成功")
except Exception as e:
    print(f"✗ 本地Ollama初始化失败: {e}")