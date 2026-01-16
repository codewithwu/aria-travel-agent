"""
Aria旅行助手 - 命令行界面
"""

import sys
import time
from typing import Optional

# 添加src目录到Python路径
sys.path.append('src')

from agents.basic_agent import TravelAssistant


class CommandLineInterface:
    """命令行交互界面"""
    
    def __init__(self):
        self.assistant: Optional[TravelAssistant] = None
        self.running = False
        self.setup_colors()
    
    def setup_colors(self):
        """设置控制台颜色（可选）"""
        try:
            # Windows颜色支持
            import colorama
            colorama.init()
            self.has_colors = True
            self.COLORS = {
                'HEADER': colorama.Fore.CYAN,
                'USER': colorama.Fore.GREEN,
                'ASSISTANT': colorama.Fore.YELLOW,
                'SYSTEM': colorama.Fore.MAGENTA,
                'ERROR': colorama.Fore.RED,
                'RESET': colorama.Style.RESET_ALL
            }
        except ImportError:
            self.has_colors = False
            self.COLORS = {k: '' for k in ['HEADER', 'USER', 'ASSISTANT', 'SYSTEM', 'ERROR', 'RESET']}
    
    def color_text(self, text: str, color_key: str) -> str:
        """为文本添加颜色"""
        return f"{self.COLORS.get(color_key, '')}{text}{self.COLORS['RESET']}"
    
    def print_header(self):
        """打印欢迎标题"""
        header = """
╔══════════════════════════════════════════════════════╗
║                  🧭 Aria旅行助手 🧭                   ║
║        基于AI的智能旅行规划助手 - 命令行版本           ║
╚══════════════════════════════════════════════════════╝
        """
        print(self.color_text(header, 'HEADER'))
    
    def print_help(self):
        """打印帮助信息"""
        help_text = """
📋 可用命令：
- 直接输入问题，与Aria聊天
- /help 或 /h    - 显示此帮助信息
- /reset 或 /r   - 重置对话历史
- /status 或 /s  - 显示当前状态
- /exit 或 /quit - 退出程序
- /new           - 创建新的助手实例
- /summary       - 显示对话摘要

💡 示例问题：
- "我想去日本旅游，有什么推荐吗？"
- "帮我规划一个3天的北京行程"
- "去欧洲旅行需要注意什么？"
- "预算1万元能去哪里玩？"
        """
        print(self.color_text(help_text, 'SYSTEM'))
    
    def print_status(self):
        """打印当前状态"""
        if self.assistant:
            status = f"""
📊 当前状态：
- 助手名称: {self.assistant.name}
- 对话历史: {len(self.assistant.conversation_history)//2} 轮对话
- 记忆长度: {len(self.assistant.conversation_history)} 条消息
            """
            print(self.color_text(status, 'SYSTEM'))
            
            # 显示最近对话
            if self.assistant.conversation_history:
                print(self.color_text("🗣️ 最近对话：", 'SYSTEM'))
                recent = self.assistant.conversation_history[-4:]  # 最近2轮对话
                for msg in recent:
                    role = "👤 用户" if msg["role"] == "user" else f"🤖 {self.assistant.name}"
                    content = msg["content"][:80] + "..." if len(msg["content"]) > 80 else msg["content"]
                    print(f"  {role}: {content}")
        else:
            print(self.color_text("❌ 助手未初始化", 'ERROR'))
    
    def initialize_assistant(self, name: str = "Aria"):
        """初始化旅行助手"""
        print(self.color_text(f"🔄 正在初始化{name}旅行助手...", 'SYSTEM'))
        try:
            self.assistant = TravelAssistant(name=name)
            print(self.color_text(f"✅ {name}旅行助手已就绪！", 'SYSTEM'))
            return True
        except Exception as e:
            print(self.color_text(f"❌ 初始化失败: {e}", 'ERROR'))
            return False
    
    def process_command(self, user_input: str) -> bool:
        """处理用户输入的命令"""
        command = user_input.strip().lower()
        
        if command in ['/exit', '/quit', 'exit', 'quit']:
            print(self.color_text("\n👋 感谢使用Aria旅行助手，再见！", 'SYSTEM'))
            return False
        
        elif command in ['/help', '/h']:
            self.print_help()
        
        elif command in ['/reset', '/r']:
            if self.assistant:
                self.assistant.reset()
                print(self.color_text("🗑️ 对话历史已重置", 'SYSTEM'))
            else:
                print(self.color_text("❌ 助手未初始化", 'ERROR'))
        
        elif command in ['/status', '/s']:
            self.print_status()
        
        elif command == '/new':
            name = input(self.color_text("请输入新助手的名字（回车使用默认Aria）: ", 'SYSTEM'))
            name = name.strip() or "Aria"
            self.initialize_assistant(name)
        
        elif command == '/summary':
            if self.assistant:
                summary = self.assistant.get_conversation_summary()
                print(self.color_text(f"\n📋 对话摘要：\n{summary}", 'SYSTEM'))
            else:
                print(self.color_text("❌ 助手未初始化", 'ERROR'))
        
        elif command.startswith('/'):
            print(self.color_text(f"❌ 未知命令: {command}", 'ERROR'))
            print(self.color_text("输入 /help 查看可用命令", 'SYSTEM'))
        
        else:
            # 普通聊天消息
            if not self.assistant:
                print(self.color_text("⚠️ 正在自动初始化助手...", 'SYSTEM'))
                self.initialize_assistant()
            
            if self.assistant:
                # 显示用户输入
                print(self.color_text(f"\n👤 你: {user_input}", 'USER'))
                
                # 显示思考提示
                print(self.color_text("🤔 思考中", 'ASSISTANT'), end="", flush=True)
                for _ in range(3):
                    time.sleep(0.3)
                    print(self.color_text(".", 'ASSISTANT'), end="", flush=True)
                print()
                
                # 获取回复
                response = self.assistant.chat(user_input)
                
                # 显示助手回复
                print(self.color_text(f"🤖 {self.assistant.name}: {response}\n", 'ASSISTANT'))
        
        return True
    
    def run(self):
        """运行主循环"""
        self.running = True
        
        # 打印标题
        self.print_header()
        
        # 初始化助手
        if not self.initialize_assistant():
            print(self.color_text("❌ 无法启动助手，程序退出", 'ERROR'))
            return
        
        # 显示帮助
        print(self.color_text("💡 输入 /help 查看可用命令\n", 'SYSTEM'))
        
        # 主循环
        while self.running:
            try:
                # 获取用户输入
                user_input = input(self.color_text("❯ ", 'HEADER')).strip()
                
                if not user_input:
                    continue
                
                # 处理命令
                self.running = self.process_command(user_input)
            
            except KeyboardInterrupt:
                print(self.color_text("\n\n⚠️ 检测到中断信号", 'ERROR'))
                confirm = input(self.color_text("确定要退出吗？(y/n): ", 'ERROR')).strip().lower()
                if confirm in ['y', 'yes', '是']:
                    print(self.color_text("👋 再见！", 'SYSTEM'))
                    break
            
            except EOFError:
                print(self.color_text("\n\n👋 检测到文件结束，退出程序", 'SYSTEM'))
                break
            
            except Exception as e:
                print(self.color_text(f"\n❌ 发生错误: {e}", 'ERROR'))
                # 继续运行，不退出
    
    def cleanup(self):
        """清理资源"""
        print(self.color_text("\n🧹 正在清理资源...", 'SYSTEM'))
        # 这里可以添加资源清理逻辑
        print(self.color_text("✅ 清理完成", 'SYSTEM'))


def main():
    """主函数"""
    cli = CommandLineInterface()
    
    try:
        cli.run()
    finally:
        cli.cleanup()


if __name__ == "__main__":
    main()
