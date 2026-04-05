#!/usr/bin/env python3
"""简化测试工具调用流式返回功能"""

from dataclasses import dataclass
from typing import Any, Callable, Optional
from threading import Lock

@dataclass
class ToolCallEvent:
    """Internal representation of a tool call event."""
    id: int
    agent: str
    tool: str
    raw_parameters: str
    parsed_parameters: dict[str, Any]
    result: str
    task_id: Optional[int]
    note_id: Optional[str]

class ToolCallTracker:
    """Collects tool call events and converts them to SSE payloads."""

    def __init__(self, notes_workspace: Optional[str]) -> None:
        self._notes_workspace = notes_workspace
        self._events: list[ToolCallEvent] = []
        self._cursor = 0
        self._lock = Lock()
        self._event_sink: Optional[Callable[[dict[str, Any]], None]] = None

    def record(self, payload: dict[str, Any]) -> None:
        """记录模型工具调用情况，便于日志与前端展示。"""

        agent_name = str(payload.get("agent_name") or "unknown")
        tool_name = str(payload.get("tool_name") or "unknown")
        raw_parameters = str(payload.get("raw_parameters") or "")
        parsed_parameters = payload.get("parsed_parameters") or {}
        result_text = str(payload.get("result") or "")
        event_type = payload.get("event_type", "tool_call")

        if not isinstance(parsed_parameters, dict):
            parsed_parameters = {}

        task_id = None
        note_id: Optional[str] = None

        event = ToolCallEvent(
            id=len(self._events) + 1,
            agent=agent_name,
            tool=tool_name,
            raw_parameters=raw_parameters,
            parsed_parameters=parsed_parameters,
            result=result_text,
            task_id=task_id,
            note_id=note_id,
        )

        with self._lock:
            self._events.append(event)

        print(
            f"Tool call recorded: agent={agent_name} tool={tool_name} event_type={event_type}"
        )

        sink = self._event_sink
        if sink:
            payload = self._build_payload(event, step=None)
            payload["event_type"] = event_type
            sink(payload)

    def _build_payload(self, event: ToolCallEvent, step: Optional[int]) -> dict[str, Any]:
        payload = {
            "type": "tool_call",
            "event_id": event.id,
            "agent": event.agent,
            "tool": event.tool,
            "parameters": event.parsed_parameters,
            "result": event.result,
            "task_id": event.task_id,
            "note_id": event.note_id,
        }
        if step is not None:
            payload["step"] = step
        return payload

    def set_event_sink(self, sink: Optional[Callable[[dict[str, Any]], None]]) -> None:
        """Register a callback for immediate tool event notifications."""
        self._event_sink = sink

# 测试ToolCallTracker的使用
print("开始测试工具调用流式返回功能...")
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
