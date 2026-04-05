import pytest
from httpx import AsyncClient
from src.main import create_app


@pytest.mark.asyncio
async def test_health_check():
    """测试健康检查端点"""
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/healthz")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_research_endpoint_validation():
    """测试研究端点的验证"""
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as client:
        # 测试缺少topic参数
        response = await client.post("/research", json={})
        assert response.status_code == 422
        
        # 测试有效参数
        response = await client.post("/research", json={"topic": "测试主题"})
        # 由于需要真实的LLM配置，这里会失败但应该不是422错误
        assert response.status_code != 422


@pytest.mark.asyncio
async def test_research_stream_endpoint_validation():
    """测试研究流端点的验证"""
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as client:
        # 测试缺少topic参数
        response = await client.post("/research/stream", json={})
        assert response.status_code == 422
        
        # 测试有效参数
        response = await client.post("/research/stream", json={"topic": "测试主题"})
        # 由于需要真实的LLM配置，这里会失败但应该不是422错误
        assert response.status_code != 422