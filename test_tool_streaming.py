#!/usr/bin/env python3
"""测试工具调用流式返回功能"""

import asyncio
from backend.src.agent import DeepResearchAgent
from backend.src.config import Configuration

async def test_tool_streaming():
    """测试工具调用流式返回"""
    print("开始测试工具调用流式返回功能...")
    
    # 创建配置
    config = Configuration.from_env()
    
    # 创建深度研究代理
    agent = DeepResearchAgent(config=config)
    
    # 测试主题
    topic = "人工智能最新发展"
    
    print(f"研究主题: {topic}")
    print("=" * 50)
    
    # 使用流式运行
    async for event in agent.run_stream(topic):
        event_type = event.get("type")
        
        # 打印不同类型的事件
        if event_type == "status":
            print(f"[状态] {event.get('message')}")
        elif event_type == "todo_list":
            tasks = event.get("tasks", [])
            print(f"[任务列表] 生成了 {len(tasks)} 个任务")
            for i, task in enumerate(tasks, 1):
                print(f"  {i}. {task.get('title')} - {task.get('intent')}")
        elif event_type == "tool_call_start":
            tool = event.get("tool")
            agent_name = event.get("agent")
            print(f"[工具调用开始] {agent_name} 正在调用 {tool} 工具")
        elif event_type == "tool_call_end":
            tool = event.get("tool")
            result = event.get("result", "")
            print(f"[工具调用结束] {tool} 工具执行完成")
            if result:
                print(f"  结果: {result[:100]}..." if len(result) > 100 else f"  结果: {result}")
        elif event_type == "task_status":
            status = event.get("status")
            task_id = event.get("task_id")
            title = event.get("title")
            print(f"[任务状态] 任务 {task_id} ({title}) 状态: {status}")
        elif event_type == "sources":
            task_id = event.get("task_id")
            sources = event.get("latest_sources", "")
            print(f"[信息源] 任务 {task_id} 收集到信息源")
        elif event_type == "task_summary_chunk":
            task_id = event.get("task_id")
            content = event.get("content")
            print(f"[总结片段] 任务 {task_id}: {content}", end="")
        elif event_type == "final_report":
            report = event.get("report", "")
            print(f"[最终报告] 生成完成")
            print(f"  报告长度: {len(report)} 字符")
        elif event_type == "done":
            print("[完成] 研究流程结束")
        
        # 添加分隔线以提高可读性
        if event_type in ["status", "todo_list", "task_status", "final_report", "done"]:
            print("-" * 50)

if __name__ == "__main__":
    asyncio.run(test_tool_streaming())
