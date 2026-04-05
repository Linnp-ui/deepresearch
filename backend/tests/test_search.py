import pytest
from src.services.search import SearchService, generate_cache_key, search_results_cache, research_context_cache


@pytest.fixture
def search_service():
    """创建搜索服务实例"""
    return SearchService()


def test_generate_cache_key():
    """测试缓存键生成功能"""
    topic = "test topic"
    cache_key = generate_cache_key(topic)
    assert isinstance(cache_key, str)
    assert len(cache_key) == 32  # MD5哈希长度


def test_search_results_cache():
    """测试搜索结果缓存功能"""
    # 清除缓存
    search_results_cache.clear()
    
    # 测试缓存设置
    cache_key = "test_cache_key"
    test_data = {"results": ["test result"]}
    search_results_cache[cache_key] = test_data
    assert cache_key in search_results_cache
    assert search_results_cache[cache_key] == test_data
    
    # 测试缓存清除
    del search_results_cache[cache_key]
    assert cache_key not in search_results_cache


def test_research_context_cache():
    """测试研究上下文缓存功能"""
    # 清除缓存
    research_context_cache.clear()
    
    # 测试缓存设置
    cache_key = "test_context_key"
    test_data = {"context": "test context"}
    research_context_cache[cache_key] = test_data
    assert cache_key in research_context_cache
    assert research_context_cache[cache_key] == test_data
    
    # 测试缓存清除
    del research_context_cache[cache_key]
    assert cache_key not in research_context_cache