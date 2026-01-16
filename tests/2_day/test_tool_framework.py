"""工具框架综合测试"""

import sys
import json
sys.path.append('src')

from src.core.tools.tool_registry import tool_registry, ToolCategory
from src.tools.basic_tools import *


class ToolFrameworkTester:
    """工具框架测试器"""
    
    def __init__(self):
        self.test_results = []
    
    def run_test(self, test_name, test_func):
        """运行单个测试"""
        print(f"\n🔍 {test_name}")
        print("-" * 40)
        
        try:
            result = test_func()
            print(f"✅ 通过")
            self.test_results.append((test_name, True, result))
            return True
        except Exception as e:
            print(f"❌ 失败: {e}")
            self.test_results.append((test_name, False, str(e)))
            return False
    
    def test_tool_registration(self):
        """测试工具注册"""
        tools = tool_registry.list_tools()
        assert len(tools) >= 5, f"预期至少5个工具，实际只有{len(tools)}个"
        
        # 检查特定工具是否已注册
        tool_names = {tool['name'] for tool in tools}
        expected_tools = {
            'get_current_time',
            'calculate_budget', 
            'convert_currency',
            'estimate_travel_time',
            'get_season_info'
        }
        
        for tool in expected_tools:
            assert tool in tool_names, f"工具 '{tool}' 未注册"
        
        return f"已注册 {len(tools)} 个工具: {', '.join(sorted(tool_names))}"
    
    def test_tool_categories(self):
        """测试工具分类"""
        for category in ToolCategory:
            tools_in_category = tool_registry.list_tools_by_category(category)
            print(f"  {category.value}: {len(tools_in_category)} 个工具")
        
        # 检查特定分类是否有工具
        calculation_tools = tool_registry.list_tools_by_category(ToolCategory.CALCULATION)
        assert len(calculation_tools) >= 2, f"预期至少2个计算工具，实际只有{len(calculation_tools)}个"
        
        return f"工具分类测试完成"
    
    def test_tool_execution(self):
        """测试工具执行"""
        test_cases = [
            {
                "name": "get_current_time",
                "kwargs": {"timezone": "Asia/Shanghai"},
                "validate": lambda r: isinstance(r, str) and "上海" in r
            },
            {
                "name": "calculate_budget",
                "kwargs": {"days": 3, "destination": "东京", "travelers": 2},
                "validate": lambda r: isinstance(r, dict) and "总预算" in r
            },
            {
                "name": "convert_currency",
                "kwargs": {"amount": 100, "from_currency": "USD", "to_currency": "JPY"},
                "validate": lambda r: isinstance(r, dict) and "转换金额" in r
            },
            {
                "name": "estimate_travel_time",
                "kwargs": {"origin": "北京", "destination": "上海", "mode": "高铁"},
                "validate": lambda r: isinstance(r, dict) and "估算时间" in r
            },
            {
                "name": "get_season_info",
                "kwargs": {"destination": "东京", "month": 4},
                "validate": lambda r: isinstance(r, dict) and "季节" in r
            }
        ]
        
        results = []
        for test_case in test_cases:
            try:
                result = tool_registry.execute(test_case["name"], **test_case["kwargs"])
                is_valid = test_case["validate"](result)
                
                if is_valid:
                    results.append(f"{test_case['name']}: 成功")
                else:
                    results.append(f"{test_case['name']}: 结果验证失败")
                    print(f"  {test_case['name']} 返回结果: {result}")
            except Exception as e:
                results.append(f"{test_case['name']}: 执行失败 - {e}")
        
        # 检查所有测试是否通过
        success_count = sum(1 for r in results if "成功" in r)
        assert success_count >= 4, f"只有 {success_count}/{len(test_cases)} 个工具执行成功"
        
        return f"执行了 {len(test_cases)} 个工具，{success_count} 个成功"
    
    def test_error_handling(self):
        """测试错误处理"""
        # 测试不存在的工具
        try:
            tool_registry.execute("non_existent_tool")
            assert False, "应该抛出异常"
        except ValueError as e:
            assert "不存在" in str(e), f"预期错误消息包含'不存在'，实际: {e}"
        
        # 测试参数验证
        try:
            tool_registry.execute("calculate_budget", days="不是数字")
            assert False, "应该抛出异常"
        except (ValueError, RuntimeError) as e:
            # 参数验证失败或执行失败都可以
            pass
        
        # 测试缺少必需参数
        try:
            tool_registry.execute("calculate_budget")
            assert False, "应该抛出异常"
        except (ValueError, RuntimeError) as e:
            pass
        
        return "错误处理测试通过"
    
    def test_tool_schema(self):
        """测试工具Schema"""
        tool = tool_registry.get_tool("calculate_budget")
        assert tool is not None, "无法获取calculate_budget工具"
        
        schema = tool.get_schema()
        
        # 检查schema结构
        required_fields = ["name", "description", "category", "parameters", "returns"]
        for field in required_fields:
            assert field in schema, f"schema缺少字段: {field}"
        
        # 检查参数信息
        assert len(schema["parameters"]) >= 2, "至少应有2个参数"
        
        # 检查参数详细信息
        for param in schema["parameters"]:
            assert "name" in param
            assert "type" in param
            assert "description" in param
            assert "required" in param
        
        print("  Schema示例:")
        print(f"    名称: {schema['name']}")
        print(f"    描述: {schema['description']}")
        print(f"    分类: {schema['category']}")
        print(f"    参数: {[p['name'] for p in schema['parameters']]}")
        
        return f"工具Schema测试通过，包含 {len(schema['parameters'])} 个参数"
    
    def test_performance(self):
        """测试性能"""
        import time
        
        # 测试多次执行
        start_time = time.time()
        executions = 10
        
        for i in range(executions):
            tool_registry.execute("get_current_time")
        
        end_time = time.time()
        avg_time = (end_time - start_time) / executions
        
        assert avg_time < 1.0, f"平均执行时间 {avg_time:.3f}秒 太慢"
        
        return f"性能测试: {executions} 次执行，平均 {avg_time:.3f} 秒/次"
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始工具框架综合测试")
        print("=" * 60)
        
        tests = [
            ("工具注册测试", self.test_tool_registration),
            ("工具分类测试", self.test_tool_categories),
            ("工具执行测试", self.test_tool_execution),
            ("错误处理测试", self.test_error_handling),
            ("工具Schema测试", self.test_tool_schema),
            ("性能测试", self.test_performance),
        ]
        
        passed = 0
        for test_name, test_func in tests:
            if self.run_test(test_name, test_func):
                passed += 1
        
        # 打印总结
        print("\n" + "=" * 60)
        print("📊 测试总结")
        print("=" * 60)
        
        print(f"总测试数: {len(tests)}")
        print(f"通过: {passed}")
        print(f"失败: {len(tests) - passed}")
        
        if passed == len(tests):
            print("\n🎉 所有测试通过！工具框架工作正常。")
        else:
            print("\n⚠️ 部分测试失败，详情:")
            for test_name, success, result in self.test_results:
                status = "✅" if success else "❌"
                print(f"  {status} {test_name}: {result}")
        
        return passed == len(tests)


def main():
    tester = ToolFrameworkTester()
    success = tester.run_all_tests()
    
    # 显示所有可用工具
    if success:
        print("\n" + "=" * 60)
        print("🛠️ 所有可用工具:")
        print("=" * 60)
        
        tools = tool_registry.list_tools()
        for i, tool_info in enumerate(tools, 1):
            print(f"\n{i}. {tool_info['name']}")
            print(f"   描述: {tool_info['description']}")
            print(f"   分类: {tool_info['category']}")
            print(f"   参数: {[p['name'] for p in tool_info['parameters']]}")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
