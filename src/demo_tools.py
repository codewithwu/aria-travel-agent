"""工具演示脚本"""

import sys
sys.path.append('src')

from src.core.tools.tool_registry import tool_registry, register_tool

from src.tools.basic_tools import *


# @register_tool(
#     name="my_tool",
#     description="我的自定义工具",
#     category=ToolCategory.UTILITY
# )
# def my_tool(param1: str, param2: int = 10) -> dict:
#     """
#     我的工具描述
    
#     Args:
#         param1: 参数1描述
#         param2: 参数2描述
#     """
#     return {"result": f"{param1} repeated {param2} times"}


def demo_tool_execution():
    """演示工具执行"""
    print("🛠️ 工具演示")
    print("=" * 50)
    
    # 演示1: 预算计算
    print("\n1. 📊 旅行预算计算")
    print("-" * 30)
    budget = tool_registry.execute(
        "calculate_budget",
        days=7,
        destination="东京",
        travelers=2,
        budget_level="中等"
    )
    
    print(f"目的地: {budget['目的地']}")
    print(f"天数: {budget['旅行天数']}天")
    print(f"人数: {budget['旅行人数']}人")
    print(f"预算级别: {budget['预算级别']}")
    print(f"每人每天: ${budget['每人每天预算']}")
    print(f"总预算: ${budget['总预算']}")
    
    print("\n详细分配:")
    for category, amount in budget['预算详情'].items():
        print(f"  {category}: ${amount}")
    
    # 演示2: 货币转换
    print("\n2. 💱 货币转换")
    print("-" * 30)
    conversion = tool_registry.execute(
        "convert_currency",
        amount=budget['总预算'],
        from_currency="USD",
        to_currency="CNY"
    )
    
    print(f"${conversion['原始金额']} USD")
    print(f"汇率: {conversion['汇率']}")
    print(f"= ¥{conversion['转换金额']} CNY")
    
    # 演示3: 旅行时间估算
    print("\n3. 🚅 旅行时间估算")
    print("-" * 30)
    travel_time = tool_registry.execute(
        "estimate_travel_time",
        origin="北京",
        destination="东京",
        mode="飞机"
    )
    
    print(f"{travel_time['出发地']} → {travel_time['目的地']}")
    print(f"交通方式: {travel_time['交通方式']}")
    print(f"距离: {travel_time['估算距离']}")
    print(f"时间: {travel_time['估算时间']}")
    
    # 演示4: 季节信息
    print("\n4. 🌸 季节信息")
    print("-" * 30)
    season_info = tool_registry.execute(
        "get_season_info",
        destination="东京",
        month=4
    )
    
    print(f"目的地: {season_info['目的地']}")
    print(f"月份: {season_info['月份']}")
    print(f"季节: {season_info['季节']}")
    print(f"特点: {season_info['特点']}")
    print(f"推荐活动: {season_info['推荐活动']}")
    
    # 演示5: 所有可用工具
    print("\n5. 📋 所有可用工具")
    print("-" * 30)
    tools = tool_registry.list_tools()
    
    print(f"共 {len(tools)} 个工具:")
    for i, tool in enumerate(tools, 1):
        param_count = len(tool['parameters'])
        print(f"  {i:2d}. {tool['name']:20} ({tool['category']:15}) - 参数: {param_count}")


def main():
    try:

        demo_tool_execution()
        print("\n" + "=" * 50)
        print("✅ 演示完成！工具框架工作正常。")
        return True
    except Exception as e:
        print(f"\n❌ 演示失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
