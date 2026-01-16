"""边界情况测试"""

import sys
# sys.path.append('src')

from src.agents.basic_agent import TravelAssistant

def test_edge_cases():
    print("🧪 边界情况测试")
    print("=" * 40)
    
    assistant = TravelAssistant()
    
    test_cases = [
        ("空输入", ""),
        ("非常长的输入", "我想去一个有很多很多好玩的地方但是又不太贵而且人不太多但是风景很美食物很好吃而且交通方便的地方旅游，你有什么推荐吗？" * 3),
        ("特殊字符", "我想去@#$%^&*()地方旅游"),
        ("英文输入", "Recommend some good places to visit in Europe"),
        ("数字输入", "1234567890"),
        ("混合输入", "我想去Paris和东京，budget约¥50000，有什么推荐？"),
    ]
    
    for case_name, user_input in test_cases:
        print(f"\n测试: {case_name}")
        print(f"输入: {user_input[:50]}..." if len(user_input) > 50 else f"输入: {user_input}")
        
        try:
            response = assistant.chat(user_input)
            print(f"响应: {response[:100]}..." if len(response) > 100 else f"响应: {response}")
            print("✅ 处理成功")
        except Exception as e:
            print(f"❌ 处理失败: {e}")
    
    # 测试记忆限制
    print("\n🧠 测试记忆限制")
    assistant.reset()
    
    for i in range(15):  # 超过20条限制
        assistant.chat(f"测试消息 {i+1}")
    
    print(f"历史消息数量: {len(assistant.conversation_history)}")
    print(f"预期最多20条，实际: {'✅ 符合' if len(assistant.conversation_history) <= 20 else '❌ 超出'}预期")
    
    # 显示部分历史
    print("\n最近5条历史:")
    for msg in assistant.conversation_history[-5:]:
        role = "用户" if msg['role'] == 'user' else "助手"
        content = msg['content'][:30] + "..." if len(msg['content']) > 30 else msg['content']
        print(f"  {role}: {content}")

if __name__ == "__main__":
    test_edge_cases()
