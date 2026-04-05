#!/usr/bin/env python3
"""测试ToolCallTracker类的工具调用流式返回功能"""

# 直接导入ToolCallTracker类，避免导入整个agent模块
import sys
import os

# 添加backend/src到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

# 直接导入所需的模块
from src.services.tool_events import ToolCallTracker
from src.models import SummaryState, TodoItem

# 测试ToolCallTracker的使用
print("开始测试ToolCallTracker工具调用流式返回功能...")
print("=" * 50)

# 创建ToolCallTracker实例
tracker = ToolCallTracker(notes_workspace="./backend/notes")

# 模拟工具调用开始事件
def tool_event_sink(event):
    """模拟事件接收器"""
    event_type = event.get("event_type", "tool_call")
    if event_type == "tool_call_start":
        print(f"[工具调用开始] {event.get('agent')} 正在调用 {event.get('tool')} 工具")
    elif event_type == "tool_call_end":
        print(f"[工具调用结束] {event.get('tool')} 工具执行完成")
        result = event.get("result", "")
        if result:
            print(f"  结果: {result[:100]}..." if len(result) > 100 else f"  结果: {result}")
    else:
        print(f"[工具调用] {event.get('tool')} 工具被调用")

# 设置事件接收器
tracker.set_event_sink(tool_event_sink)

# 模拟工具调用开始
tracker.record({
    "agent_name": "研究规划专家",
    "tool_name": "note",
    "raw_parameters": "{\"action\": \"create\", \"title\": \"测试笔记\", \"content\": \"这是一个测试笔记\"}",
    "parsed_parameters": {"action": "create", "title": "测试笔记", "content": "这是一个测试笔记"},
    "result": "",
    "event_type": "tool_call_start"
})

# 模拟工具调用结束
tracker.record({
    "agent_name": "研究规划专家",
    "tool_name": "note",
    "raw_parameters": "{\"action\": \"create\", \"title\": \"测试笔记\", \"content\": \"这是一个测试笔记\"}",
    "parsed_parameters": {"action": "create", "title": "测试笔记", "content": "这是一个测试笔记"},
    "result": "✅ 笔记创建成功！ID: note_20260403_123456_0",
    "event_type": "tool_call_end"
})

# 模拟另一个工具调用
tracker.record({
    "agent_name": "任务总结专家",
    "tool_name": "note",
    "raw_parameters": "{\"action\": \"update\", \"note_id\": \"note_20260403_123456_0\", \"content\": \"更新后的测试笔记\"}",
    "parsed_parameters": {"action": "update", "note_id": "note_20260403_123456_0", "content": "更新后的测试笔记"},
    "result": "✅ 笔记更新成功！",
    "event_type": "tool_call"
})

print("=" * 50)
print("测试完成！")
