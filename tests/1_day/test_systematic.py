"""系统化测试脚本"""

import sys
import time
# sys.path.append('src')

from src.agents.basic_agent import TravelAssistant

class SystemTester:
    def __init__(self):
        self.assistant = TravelAssistant()
        self.test_results = []
        
    def run_test(self, test_name, test_func):
        """运行单个测试"""
        print(f"\n🔍 运行测试: {test_name}")
        print("-" * 40)
        
        start_time = time.time()
        try:
            result = test_func()
            end_time = time.time()
            elapsed = end_time - start_time
            
            test_result = {
                'name': test_name,
                'status': 'PASS',
                'elapsed': elapsed,
                'result': result
            }
            self.test_results.append(test_result)
            print(f"✅ 测试通过 ({elapsed:.2f}s)")
            return True
            
        except Exception as e:
            end_time = time.time()
            elapsed = end_time - start_time
            
            test_result = {
                'name': test_name,
                'status': 'FAIL',
                'elapsed': elapsed,
                'error': str(e)
            }
            self.test_results.append(test_result)
            print(f"❌ 测试失败: {e} ({elapsed:.2f}s)")
            return False
    
    def test_initialization(self):
        """测试助手初始化"""
        assert self.assistant.name == "Aria", "助手名称错误"
        assert hasattr(self.assistant, 'system_prompt'), "缺少system_prompt属性"
        assert isinstance(self.assistant.conversation_history, list), "对话历史不是列表"
        return "助手初始化成功"
    
    def test_single_chat(self):
        """测试单次对话"""
        response = self.assistant.chat("你好")
        assert isinstance(response, str), "响应不是字符串"
        assert len(response) > 0, "响应为空"
        assert "aria" in response or "旅行" in response, "响应内容不符合预期"
        return f"单次对话测试成功，响应长度: {len(response)}字符"
    
    def test_multi_turn_chat(self):
        """测试多轮对话"""
        # 第一轮
        self.assistant.reset()
        response1 = self.assistant.chat("我想去日本旅游")
        assert len(response1) > 0, "第一轮响应为空"
        
        # 第二轮（应该能记住上下文）
        response2 = self.assistant.chat("有什么具体推荐吗？")
        assert len(response2) > 0, "第二轮响应为空"

        print(f"w {len(self.assistant.conversation_history)}")
        print("###")
        print(f"w {self.assistant.conversation_history}")
        print("###")
        
        # 检查对话历史
        assert len(self.assistant.conversation_history) == 4, "对话历史记录不正确"
        
        return f"多轮对话测试成功，历史记录: {len(self.assistant.conversation_history)}条消息"
    
    def test_conversation_reset(self):
        """测试对话重置"""
        # 先进行一些对话
        self.assistant.chat("测试消息")
        initial_count = len(self.assistant.conversation_history)
        
        # 重置
        self.assistant.reset()
        
        # 验证重置
        assert len(self.assistant.conversation_history) == 0, "重置后对话历史不为空"
        
        return f"重置测试成功，重置前: {initial_count}条，重置后: 0条"
    
    def test_chinese_response(self):
        """测试中文响应"""
        response = self.assistant.chat("用中文回答：今天天气怎么样？")
        # 简单检查是否包含中文字符
        has_chinese = any('\u4e00' <= char <= '\u9fff' for char in response)
        assert has_chinese, "响应可能不包含中文"
        return f"中文响应测试成功，响应长度: {len(response)}字符"
    
    def test_temperature_effect(self):
        """测试温度参数影响"""
        response1 = self.assistant.chat("讲一个短笑话", temperature=0.2)
        response2 = self.assistant.chat("讲一个短笑话", temperature=0.9)
        
        # 不能保证不同，但至少应该有响应
        assert len(response1) > 0 and len(response2) > 0, "温度参数测试失败"
        
        return f"温度参数测试成功，响应1长度: {len(response1)}，响应2长度: {len(response2)}"
    
    def print_summary(self):
        """打印测试摘要"""
        print("\n" + "=" * 60)
        print("测试摘要")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r['status'] == 'PASS')
        failed_tests = total_tests - passed_tests
        
        print(f"总测试数: {total_tests}")
        print(f"通过: {passed_tests}")
        print(f"失败: {failed_tests}")
        
        total_time = sum(r['elapsed'] for r in self.test_results)
        print(f"总耗时: {total_time:.2f}秒")
        print(f"平均每个测试: {total_time/total_tests:.2f}秒")
        
        if failed_tests > 0:
            print("\n❌ 失败测试详情:")
            for test in self.test_results:
                if test['status'] == 'FAIL':
                    print(f"  - {test['name']}: {test.get('error', '未知错误')}")
        
        return passed_tests == total_tests
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始系统化测试")
        print("=" * 60)
        
        tests = [
            ("初始化测试", self.test_initialization),
            ("单次对话测试", self.test_single_chat),
            ("多轮对话测试", self.test_multi_turn_chat),
            ("对话重置测试", self.test_conversation_reset),
            ("中文响应测试", self.test_chinese_response),
            ("温度参数测试", self.test_temperature_effect),
        ]
        
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
        
        return self.print_summary()

def main():
    tester = SystemTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 所有测试通过！Day 1开发完成。")
    else:
        print("\n⚠️  部分测试失败，请检查问题。")
    
    return success

if __name__ == "__main__":
    main()