# 创建文件 src/core/llm_client.py
import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """统一的LLM客户端，支持多种模型提供商"""
    
    def __init__(self, 
                 provider:str = "ollama", 
                 temperature:float=0, 
                 max_tokens:int=2000, 
                 timeout:int=30):
        
        self.provider = provider or os.getenv('LLM_PROVIDER', 'ollama').lower()
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self._setup_clients()
    
    def _setup_clients(self):
        """根据配置初始化客户端"""
        if self.provider == 'zhipu':
            self._setup_zhipu()
        elif self.provider == 'ollama':
            self._setup_ollama()
        else:
            raise ValueError(f"不支持的LLM提供商: {self.provider}")
    
    def _setup_zhipu(self):
        """初始化智普客户端"""
        try:
            from langchain_openai import ChatOpenAI
            api_key = os.getenv('ZHIPU_API_KEY')
            base_url = os.getenv('ZHIPU_BASEURL')
            model_name = os.getenv('ZHIPU_MODEL_NAME')
            if not all([api_key, base_url, model_name]):
                raise ValueError("智谱API配置缺失")
            
            self.client = ChatOpenAI(
            model=model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            timeout=self.timeout,
            api_key=api_key,
            base_url=base_url,
        )
            print(f"✓ 已初始化OpenAI客户端，使用模型: {self.model}")
        except ImportError:
            raise ImportError("请安装openai包: pip install langchain_openai")
    
    def _setup_ollama(self):
        """初始化Ollama客户端"""
        try:
            from langchain_ollama import ChatOllama
            model_name = os.getenv('OLLAMA_MODEL_NAME')
            base_url = os.getenv('OLLAMA_BASEURL')
            if not all([base_url, model_name]):
                raise ValueError("OllamaAPI配置缺失")
            
            self.client = ChatOllama(
                        model=model_name,
                        base_url=base_url,
                        temperature=self.temperature,
                        max_tokens=self.max_tokens,
                        timeout=self.timeout,
                    )
            print(f"✓ 已初始化Ollama客户端，使用模型: {model_name}")
        except ImportError:
            raise ImportError("请安装ollama包: pip install langchain_ollama")
    


# 创建全局客户端实例（方便使用）
llm_client = LLMClient()


def test_llm_client():
    """测试LLM客户端"""
    print("测试LLM客户端...")
    
    # 测试简单的对话
    test_prompt = "你好，请用一句话介绍你自己。"
    system_msg = "你是一个友好的AI助手。"

    messages = [
                    (
                        "system",
                        system_msg,
                    ),
                    ("human", test_prompt),
                ]
    
    print(f"用户: {test_prompt}")
    response = llm_client.client.invoke(messages)
    print(f"AI助手: {response.content}")
    
    return response


if __name__ == "__main__":
    test_llm_client()
