"""
基础旅行工具
"""

import datetime
import random
from typing import Dict, List, Optional, Tuple
from src.core.tools.tool_registry import register_tool, ToolCategory


@register_tool(
    name="get_current_time",
    description="获取当前时间和日期",
    category=ToolCategory.UTILITY,
    return_description="当前日期时间字符串"
)
def get_current_time(timezone: str = "Asia/Shanghai") -> str:
    """
    获取指定时区的当前时间
    
    Args:
        timezone: 时区名称，默认为"Asia/Shanghai"
        
    Returns:
        格式化的日期时间字符串
    """
    # 注意：这里简化处理，实际应该使用时区库
    now = datetime.datetime.now()
    
    # 模拟时区偏移（简化处理）
    timezone_offsets = {
        "Asia/Shanghai": 8,
        "Asia/Tokyo": 9,
        "Europe/London": 0,
        "America/New_York": -5,
        "America/Los_Angeles": -8
    }
    
    offset = timezone_offsets.get(timezone, 8)
    adjusted_time = now + datetime.timedelta(hours=offset)
    
    return adjusted_time.strftime(f"%Y年%m月%d日 %H:%M:%S ({timezone} UTC{'+' if offset >= 0 else ''}{offset})")


@register_tool(
    name="calculate_budget",
    description="计算旅行预算",
    category=ToolCategory.CALCULATION,
    return_description="详细的预算分析"
)
def calculate_budget(
    days: int,
    destination: str,
    travelers: int = 1,
    budget_level: str = "中等"
) -> Dict[str, float]:
    """
    计算指定目的地的旅行预算
    
    Args:
        days: 旅行天数
        destination: 目的地
        travelers: 旅行者人数
        budget_level: 预算级别（经济/中等/豪华）
        
    Returns:
        包含各项预算的字典
    """
    # 目的地基准价格（美元/天/人）
    base_prices = {
        "东京": 150,
        "巴黎": 200,
        "纽约": 250,
        "曼谷": 80,
        "巴厘岛": 100,
        "悉尼": 180,
        "伦敦": 220,
        "新加坡": 160
    }
    
    # 预算级别乘数
    level_multipliers = {
        "经济": 0.7,
        "中等": 1.0,
        "豪华": 1.8
    }
    
    # 获取基准价格
    base_price = base_prices.get(destination, 120)
    multiplier = level_multipliers.get(budget_level, 1.0)
    
    # 计算各项预算
    daily_price = base_price * multiplier
    
    # 预算分配比例
    allocation = {
        "住宿": 0.35,
        "餐饮": 0.25,
        "交通": 0.20,
        "景点门票": 0.15,
        "购物其他": 0.05
    }
    
    total_budget = daily_price * days * travelers
    
    detailed_budget = {
        "目的地": destination,
        "旅行天数": days,
        "旅行人数": travelers,
        "预算级别": budget_level,
        "每人每天预算": round(daily_price, 2),
        "总预算": round(total_budget, 2),
        "预算详情": {}
    }
    
    for category, ratio in allocation.items():
        amount = total_budget * ratio
        detailed_budget["预算详情"][category] = round(amount, 2)
    
    return detailed_budget


@register_tool(
    name="convert_currency",
    description="货币转换",
    category=ToolCategory.CALCULATION,
    return_description="转换后的金额"
)
def convert_currency(
    amount: float,
    from_currency: str = "USD",
    to_currency: str = "CNY"
) -> Dict[str, float]:
    """
    货币转换
    
    Args:
        amount: 要转换的金额
        from_currency: 源货币代码
        to_currency: 目标货币代码
        
    Returns:
        转换结果
    """
    # 模拟汇率（这里使用固定值，实际应该调用API）
    exchange_rates = {
        "USD": {"CNY": 7.2, "JPY": 150, "EUR": 0.92, "GBP": 0.79},
        "CNY": {"USD": 0.14, "JPY": 21, "EUR": 0.13, "GBP": 0.11},
        "JPY": {"USD": 0.0067, "CNY": 0.048, "EUR": 0.0061, "GBP": 0.0052},
        "EUR": {"USD": 1.09, "CNY": 7.85, "JPY": 163, "GBP": 0.86},
        "GBP": {"USD": 1.27, "CNY": 9.15, "JPY": 190, "EUR": 1.16}
    }
    
    # 确保货币代码大写
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    
    # 获取汇率
    if (from_currency in exchange_rates and 
        to_currency in exchange_rates[from_currency]):
        rate = exchange_rates[from_currency][to_currency]
        converted_amount = amount * rate
        
        return {
            "原始金额": amount,
            "原始货币": from_currency,
            "目标货币": to_currency,
            "汇率": round(rate, 4),
            "转换金额": round(converted_amount, 2)
        }
    else:
        # 如果不支持的货币，返回近似值
        return {
            "原始金额": amount,
            "原始货币": from_currency,
            "目标货币": to_currency,
            "汇率": 1.0,  # 默认汇率
            "转换金额": amount,
            "备注": "使用默认汇率，实际请查询最新汇率"
        }


@register_tool(
    name="estimate_travel_time",
    description="估算旅行时间",
    category=ToolCategory.TRANSPORTATION,
    return_description="旅行时间估算"
)
def estimate_travel_time(
    origin: str,
    destination: str,
    mode: str = "飞机"
) -> Dict[str, str]:
    """
    估算两地之间的旅行时间
    
    Args:
        origin: 出发地
        destination: 目的地
        mode: 交通方式（飞机/高铁/汽车）
        
    Returns:
        时间估算结果
    """
    # 模拟距离矩阵（公里）
    distances = {
        ("北京", "上海"): 1318,
        ("北京", "广州"): 2123,
        ("上海", "广州"): 1454,
        ("东京", "大阪"): 553,
        ("纽约", "洛杉矶"): 3945,
        ("伦敦", "巴黎"): 344,
        ("北京", "东京"): 2100,
        ("上海", "东京"): 1770,
    }
    
    # 查找距离（支持两种顺序）
    key = (origin, destination)
    reverse_key = (destination, origin)
    
    distance = None
    for k in [key, reverse_key]:
        if k in distances:
            distance = distances[k]
            break
    
    # 如果没找到，使用随机距离
    if distance is None:
        distance = random.randint(500, 5000)
    
    # 不同交通方式的平均速度（km/h）
    speeds = {
        "飞机": 800,
        "高铁": 300,
        "汽车": 80,
        "火车": 120
    }
    
    speed = speeds.get(mode, 100)
    
    # 计算基础时间
    base_hours = distance / speed
    
    # 添加额外时间（安检、候车等）
    extra_time = {
        "飞机": 3.0,  # 提前到达机场+安检
        "高铁": 1.0,
        "汽车": 0.5,
        "火车": 1.5
    }
    
    total_hours = base_hours + extra_time.get(mode, 1.0)
    
    # 格式化输出
    if total_hours < 1:
        time_str = f"{int(total_hours * 60)}分钟"
    elif total_hours < 24:
        hours = int(total_hours)
        minutes = int((total_hours - hours) * 60)
        time_str = f"{hours}小时{minutes}分钟"
    else:
        days = int(total_hours / 24)
        hours = int(total_hours % 24)
        time_str = f"{days}天{hours}小时"
    
    return {
        "出发地": origin,
        "目的地": destination,
        "交通方式": mode,
        "估算距离": f"{distance}公里",
        "估算时间": time_str,
        "总小时数": round(total_hours, 1)
    }


@register_tool(
    name="get_season_info",
    description="获取目的地的季节信息",
    category=ToolCategory.INFORMATION,
    return_description="季节特点和推荐"
)
def get_season_info(
    destination: str,
    month: Optional[int] = None
) -> Dict[str, str]:
    """
    获取目的地的季节信息
    
    Args:
        destination: 目的地
        month: 月份（1-12），如果不提供则返回所有季节信息
        
    Returns:
        季节信息
    """
    # 目的地的季节特点
    seasons_data = {
        "东京": {
            "春季 (3-5月)": "樱花盛开，气候宜人，最佳旅游季节",
            "夏季 (6-8月)": "炎热潮湿，有花火大会，适合室内活动",
            "秋季 (9-11月)": "枫叶季节，天气凉爽，适合户外活动",
            "冬季 (12-2月)": "寒冷干燥，可滑雪，适合温泉旅行"
        },
        "巴黎": {
            "春季 (3-5月)": "气候温和，鲜花盛开，游客较少",
            "夏季 (6-8月)": "旅游旺季，天气温暖，适合户外咖啡",
            "秋季 (9-11月)": "天气凉爽，树叶变色，浪漫季节",
            "冬季 (12-2月)": "寒冷但节日气氛浓厚，圣诞市场"
        },
        "曼谷": {
            "凉季 (11-2月)": "最佳旅游季节，气候凉爽干燥",
            "热季 (3-5月)": "非常炎热，注意防暑",
            "雨季 (6-10月)": "经常下雨，但物价较低"
        },
        "悉尼": {
            "夏季 (12-2月)": "海滩季节，适合水上活动",
            "秋季 (3-5月)": "天气温和，适合户外活动",
            "冬季 (6-8月)": "凉爽但阳光充足，适合城市游览",
            "春季 (9-11月)": "野花盛开，气候宜人"
        }
    }
    
    # 默认目的地
    default_seasons = {
        "春季 (3-5月)": "气候温和，适合旅行",
        "夏季 (6-8月)": "旅游旺季，天气温暖",
        "秋季 (9-11月)": "天气凉爽，风景优美",
        "冬季 (12-2月)": "寒冷季节，可能有雪"
    }
    
    # 获取目的地的季节信息
    destination_seasons = seasons_data.get(destination, default_seasons)
    
    if month:
        # 根据月份确定季节
        if 3 <= month <= 5:
            season = "春季"
        elif 6 <= month <= 8:
            season = "夏季"
        elif 9 <= month <= 11:
            season = "秋季"
        else:
            season = "冬季"
        
        # 查找匹配的季节信息
        for season_key, description in destination_seasons.items():
            if season in season_key:
                return {
                    "目的地": destination,
                    "月份": f"{month}月",
                    "季节": season_key,
                    "特点": description,
                    "推荐活动": _get_recommended_activities(destination, season)
                }
    
    # 返回所有季节信息
    return {
        "目的地": destination,
        "所有季节": destination_seasons,
        "最佳旅行时间": _get_best_time_to_visit(destination)
    }


def _get_recommended_activities(destination: str, season: str) -> str:
    """获取推荐活动（内部函数）"""
    activities = {
        "东京": {
            "春季": "赏樱花、逛公园、日式庭院游览",
            "夏季": "花火大会、神社祭典、室内购物",
            "秋季": "赏红叶、登山、温泉旅行",
            "冬季": "滑雪、温泉、圣诞灯光秀"
        },
        "巴黎": {
            "春季": "公园野餐、博物馆参观、塞纳河漫步",
            "夏季": "户外咖啡、音乐节、巴黎海滩",
            "秋季": "葡萄园游览、艺术展览、美食节",
            "冬季": "圣诞市场、滑冰场、室内音乐会"
        }
    }
    
    dest_activities = activities.get(destination, {})
    return dest_activities.get(season, "城市观光、美食体验、文化探索")


def _get_best_time_to_visit(destination: str) -> str:
    """获取最佳旅行时间（内部函数）"""
    best_times = {
        "东京": "春季（3-5月）和秋季（9-11月）",
        "巴黎": "春季（4-6月）和秋季（9-10月）",
        "曼谷": "凉季（11-2月）",
        "悉尼": "春季（9-11月）和秋季（3-5月）"
    }
    return best_times.get(destination, "春季和秋季")


def test_basic_tools():
    """测试基础工具"""
    print("🧪 测试基础旅行工具")
    print("=" * 40)
    
    from src.core.tools.tool_registry import tool_registry
    
    # 列出所有已注册的工具
    print("📝 已注册的工具:")
    tools = tool_registry.list_tools()
    for i, tool_info in enumerate(tools, 1):
        print(f"  {i}. {tool_info['name']}: {tool_info['description']}")
    
    # 测试几个工具
    test_cases = [
        ("get_current_time", {"timezone": "Asia/Shanghai"}),
        ("calculate_budget", {"days": 7, "destination": "东京", "travelers": 2}),
        ("convert_currency", {"amount": 1000, "from_currency": "USD", "to_currency": "CNY"}),
        ("estimate_travel_time", {"origin": "北京", "destination": "上海", "mode": "高铁"}),
        ("get_season_info", {"destination": "东京", "month": 4}),
    ]
    
    print("\n⚙️ 测试工具执行:")
    for tool_name, kwargs in test_cases:
        print(f"\n🔧 {tool_name}:")
        try:
            result = tool_registry.execute(tool_name, **kwargs)
            print(f"  参数: {kwargs}")
            print(f"  结果: {result}")
            print("  ✅ 成功")
        except Exception as e:
            print(f"  ❌ 失败: {e}")
    
    print(f"\n✅ 总共测试了 {len(test_cases)} 个工具")


if __name__ == "__main__":
    test_basic_tools()
