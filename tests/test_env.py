import os
from dotenv import load_dotenv

load_dotenv()

# Ollama本地配置
OLLAMA_BASEURL=os.getenv('OLLAMA_BASEURL')
OLLAMA_MODEL_NAME=os.getenv('OLLAMA_MODEL_NAME')

# 智普模型
ZHIPU_API_KEY=os.getenv('ZHIPU_API_KEY')
ZHIPU_MODEL_NAME=os.getenv('ZHIPU_MODEL_NAME')
ZHIPU_BASEURL=os.getenv('ZHIPU_BASEURL')

print("环境变量测试:")
print(f"LLM_PROVIDER: {os.getenv('LLM_PROVIDER')}")
print(f"OLLAMA_BASEURL 是否存在: {'是' if os.getenv('OLLAMA_BASEURL') else '否'}")
print(f"OLLAMA_MODEL_NAME 是否存在: {'是' if os.getenv('OLLAMA_MODEL_NAME') else '否'}")



# 测试智普客户端（可选）
try:
    from langchain_openai import ChatOpenAI
    model = ChatOpenAI(
            model=ZHIPU_MODEL_NAME,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=ZHIPU_API_KEY,
            base_url=ZHIPU_BASEURL,
        )
    print("✓ OpenAI客户端初始化成功")
except Exception as e:
    print(f"✗ OpenAI客户端初始化失败: {e}")

try:
    from langchain_ollama import ChatOllama
    model = ChatOllama(
            model=OLLAMA_MODEL_NAME,
            base_url=OLLAMA_BASEURL,
            validate_model_on_init=True,
            temperature=0.8,
            num_predict=256,
        )
    print("✓ 本地Ollama客户端初始化成功")
except Exception as e:
    print(f"✗ 本地Ollama初始化失败: {e}")