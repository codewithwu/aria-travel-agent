"""
工具注册与调用框架
"""

import inspect
import functools
from typing import Dict, List, Any, Callable, Optional, get_type_hints
from dataclasses import dataclass
from enum import Enum


class ToolCategory(Enum):
    """工具分类"""
    TRAVEL = "travel"
    CALCULATION = "calculation"
    INFORMATION = "information"
    UTILITY = "utility"
    WEATHER = "weather"
    TRANSPORTATION = "transportation"
    ACCOMMODATION = "accommodation"


@dataclass
class ParameterSchema:
    """参数模式定义"""
    name: str
    type: type
    description: str
    required: bool = True
    default: Any = None


@dataclass
class Tool:
    """工具定义"""
    name: str
    function: Callable
    description: str
    category: ToolCategory
    parameters: List[ParameterSchema]
    return_type: type
    return_description: str
    
    def __call__(self, *args, **kwargs) -> Any:
        """调用工具"""
        return self.function(*args, **kwargs)
    
    def get_schema(self) -> Dict[str, Any]:
        """获取工具的JSON Schema描述"""
        schema = {
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "parameters": [
                {
                    "name": param.name,
                    "type": param.type.__name__,
                    "description": param.description,
                    "required": param.required,
                    "default": param.default
                }
                for param in self.parameters
            ],
            "returns": {
                "type": self.return_type.__name__,
                "description": self.return_description
            }
        }
        return schema
    
    def validate_arguments(self, **kwargs) -> bool:
        """验证参数"""
        for param in self.parameters:
            if param.required and param.name not in kwargs:
                return False
            if param.name in kwargs:
                # 简单的类型检查
                value = kwargs[param.name]
                if not isinstance(value, param.type):
                    try:
                        # 尝试类型转换
                        if param.type == str:
                            kwargs[param.name] = str(value)
                        elif param.type == int:
                            kwargs[param.name] = int(value)
                        elif param.type == float:
                            kwargs[param.name] = float(value)
                        elif param.type == bool:
                            kwargs[param.name] = bool(value)
                    except (ValueError, TypeError):
                        return False
        return True


class ToolRegistry:
    """工具注册表"""
    
    def __init__(self):
        self._tools: Dict[str, Tool] = {}
        self._categories: Dict[ToolCategory, List[str]] = {
            category: [] for category in ToolCategory
        }
    
    def register(self, 
                name: Optional[str] = None,
                description: str = "",
                category: ToolCategory = ToolCategory.UTILITY,
                return_description: str = "") -> Callable:
        """
        工具注册装饰器
        
        Args:
            name: 工具名称（默认使用函数名）
            description: 工具描述
            category: 工具分类
            return_description: 返回结果描述
        """
        def decorator(func: Callable) -> Callable:
            # 获取工具名称
            tool_name = name or func.__name__
            
            # 获取参数信息
            sig = inspect.signature(func)
            type_hints = get_type_hints(func)
            
            parameters = []
            for param_name, param in sig.parameters.items():
                # 跳过self参数
                if param_name == 'self':
                    continue
                    
                param_type = type_hints.get(param_name, str)
                param_desc = func.__doc__ or ""
                
                # 从docstring中提取参数描述（简化版本）
                if func.__doc__:
                    for line in func.__doc__.split('\n'):
                        if f"{param_name}:" in line:
                            param_desc = line.split(":")[1].strip()
                            break
                
                param_schema = ParameterSchema(
                    name=param_name,
                    type=param_type,
                    description=param_desc,
                    required=(param.default == inspect.Parameter.empty),
                    default=param.default if param.default != inspect.Parameter.empty else None
                )
                parameters.append(param_schema)
            
            # 获取返回类型
            return_type = type_hints.get('return', str)
            
            # 创建工具实例
            tool = Tool(
                name=tool_name,
                function=func,
                description=description or func.__doc__ or "",
                category=category,
                parameters=parameters,
                return_type=return_type,
                return_description=return_description
            )
            
            # 注册工具
            self._tools[tool_name] = tool
            self._categories[category].append(tool_name)
            
            # 保留原始函数
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            
            # 添加工具属性
            wrapper.tool = tool
            
            return wrapper
        
        return decorator
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """获取工具"""
        return self._tools.get(name)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """列出所有工具"""
        return [tool.get_schema() for tool in self._tools.values()]
    
    def list_tools_by_category(self, category: ToolCategory) -> List[Dict[str, Any]]:
        """按分类列出工具"""
        tool_names = self._categories.get(category, [])
        return [
            self._tools[name].get_schema() 
            for name in tool_names 
            if name in self._tools
        ]
    
    def execute(self, tool_name: str, **kwargs) -> Any:
        """执行工具"""
        tool = self.get_tool(tool_name)
        if not tool:
            raise ValueError(f"工具 '{tool_name}' 不存在")
        
        if not tool.validate_arguments(**kwargs):
            raise ValueError(f"工具 '{tool_name}' 参数验证失败")
        
        try:
            return tool(**kwargs)
        except Exception as e:
            raise RuntimeError(f"执行工具 '{tool_name}' 时出错: {e}")
    
    def clear(self):
        """清空注册表"""
        self._tools.clear()
        for category in self._categories:
            self._categories[category].clear()


# 创建全局工具注册表实例
tool_registry = ToolRegistry()


# 方便的装饰器别名
register_tool = tool_registry.register


def test_tool_registry():
    """测试工具注册框架"""
    print("🧪 测试工具注册框架")
    print("=" * 40)
    
    # 创建一个测试工具
    @register_tool(
        name="test_tool",
        description="一个测试工具",
        category=ToolCategory.UTILITY,
        return_description="测试结果"
    )
    def test_tool(message: str, repeat: int = 1) -> str:
        """
        测试工具
        
        Args:
            message: 要重复的消息
            repeat: 重复次数
            
        Returns:
            重复的消息字符串
        """
        return " ".join([message] * repeat)
    
    # 测试工具注册
    print("📝 已注册工具:")
    for tool_info in tool_registry.list_tools():
        print(f"  - {tool_info['name']}: {tool_info['description']}")
    
    # 测试工具执行
    print("\n⚙️ 测试工具执行:")
    try:
        result = tool_registry.execute("test_tool", message="Hello", repeat=3)
        print(f"  结果: {result}")
        print("  ✅ 工具执行成功")
    except Exception as e:
        print(f"  ❌ 工具执行失败: {e}")
    
    # 测试工具schema
    print("\n📋 工具Schema:")
    tool = tool_registry.get_tool("test_tool")
    if tool:
        schema = tool.get_schema()
        print(f"  名称: {schema['name']}")
        print(f"  描述: {schema['description']}")
        print(f"  分类: {schema['category']}")
        print(f"  参数: {[p['name'] for p in schema['parameters']]}")
    
    # 清理测试工具
    tool_registry.clear()
    print("\n🧹 测试完成，已清理注册表")


if __name__ == "__main__":
    test_tool_registry()
