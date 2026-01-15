
from typing import Optional, List, Dict, Any
from src.core.llm_client import LLMClient


class TravelAssistant:
    """基础旅行助手Agent"""
    
    def __init__(self, name: str = "Aria"):
        self.name = name
        self.system_prompt = self._create_system_prompt()
        self.conversation_history: List[Dict[str, str]] = []
        self.client = LLMClient().get_clients()
        
        print(f"✨ {self.name}旅行助手已初始化")
    
    def _create_system_prompt(self) -> str:
        """创建系统提示词"""
        return f"""你是一位专业的旅行助手，名叫{self.name}。你热情、细心、知识渊博。

        你的能力：
        1. 提供旅行建议和推荐
        2. 帮助规划行程
        3. 回答关于目的地的问题
        4. 给出预算建议
        5. 提醒旅行注意事项

        回答风格：
        - 友好、热情、有帮助
        - 提供具体、实用的建议
        - 当信息不足时，诚实地说明
        - 一次专注于回答一个问题
        - 使用适当的emoji让回答更生动

        请用中文回答所有问题。"""
    
    def chat(self, 
             user_message: str,
             reset_conversation: bool = False,
             temperature: float = 0.7) -> str:
        """
        与用户聊天
        
        Args:
            user_message: 用户消息
            reset_conversation: 是否重置对话历史
            temperature: 温度参数
            
        Returns:
            AI助手的回复
        """
        # 如果需要重置对话历史
        if reset_conversation:
            self.conversation_history = []
            print("对话历史已重置")
        
        # 构建消息列表
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # 添加历史对话（最后5轮）
        history_to_include = self.conversation_history[-10:]  # 最多10条历史消息
        messages.extend(history_to_include)
        
        # 添加当前用户消息
        messages.append({"role": "user", "content": user_message})
        
        # 调用LLM
        print(f"\n📝 用户: {user_message}")
        print("🤖 思考中...")
        
        try:
            response = self.client.invoke(messages)
            
            # 保存到对话历史
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": response.content})
            
            # 限制历史记录长度（最多保存20条消息）
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            print(f"💡 {self.name}: {response.content[:100]}...")  # 只打印前100字符
            return response.content
            
        except Exception as e:
            error_msg = f"抱歉，我暂时遇到了问题：{str(e)}"
            print(f"错误: {error_msg}")
            return error_msg
    
    def reset(self):
        """重置对话"""
        self.conversation_history = []
        print(f"🔄 {self.name}的对话历史已重置")
    
    def get_conversation_summary(self) -> str:
        """获取对话摘要"""
        if not self.conversation_history:
            return "对话历史为空"
        
        summary = f"最近对话摘要（共{len(self.conversation_history)}条消息）:\n"
        for i, msg in enumerate(self.conversation_history[-6:], 1):  # 最近6条
            role = "用户" if msg["role"] == "user" else self.name
            content_preview = msg["content"][:50] + "..." if len(msg["content"]) > 50 else msg["content"]
            summary += f"{i}. {role}: {content_preview}\n"
        
        return summary


# 创建全局助手实例
travel_assistant = TravelAssistant()


def test_basic_agent():
    """测试基础Agent"""
    print("=" * 50)
    print("测试基础旅行助手Agent")
    print("=" * 50)
    
    assistant = TravelAssistant()
    
    # 测试对话
    test_messages = [
        "你好，请介绍一下你自己",
        "我想去日本旅游，有什么建议吗？",
        "预算大概需要多少？",
        "你叫什么名字"
    ]
    
    for msg in test_messages:
        print(f"\n[用户] {msg}")
        response = assistant.chat(msg)
        print(f"[{assistant.name}] {response[:150]}...")  # 显示前150字符
    
    # 显示对话摘要
    print("\n" + "=" * 50)
    print(assistant.get_conversation_summary())
    
    return assistant


if __name__ == "__main__":
    test_basic_agent()
