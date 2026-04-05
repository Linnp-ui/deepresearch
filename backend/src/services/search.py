"""Search dispatch helpers leveraging HelloAgents SearchTool."""

from __future__ import annotations

import logging
import hashlib
from typing import Any, Optional, Tuple
from functools import lru_cache

from hello_agents.tools import SearchTool

from ..config import Configuration
from ..utils import (
    deduplicate_and_format_sources,
    format_sources,
    get_config_value,
)

logger = logging.getLogger(__name__)

MAX_TOKENS_PER_SOURCE = 2000

# 缓存配置
SEARCH_CACHE_MAX_SIZE = 100  # 最大缓存条目数
SEARCH_CACHE_TTL = 3600  # 缓存过期时间（秒）


def _generate_search_cache_key(query: str, search_api: str, fetch_full_page: bool, loop_count: int) -> str:
    """生成搜索缓存键"""
    cache_input = f"{query}:{search_api}:{fetch_full_page}:{loop_count}"
    return hashlib.md5(cache_input.encode()).hexdigest()

# 搜索结果缓存
search_cache: dict[str, tuple[float, tuple[dict[str, Any] | None, list[str], Optional[str], str]]] = {}


def dispatch_search(
    query: str,
    config: Configuration,
    loop_count: int,
) -> Tuple[dict[str, Any] | None, list[str], Optional[str], str]:
    """Execute configured search backend and normalise response payload."""

    import time
    search_api = get_config_value(config.search_api)
    
    # 生成缓存键
    cache_key = _generate_search_cache_key(query, search_api, config.fetch_full_page, loop_count)
    
    # 检查缓存
    current_time = time.time()
    if cache_key in search_cache:
        cache_time, cached_result = search_cache[cache_key]
        if current_time - cache_time < SEARCH_CACHE_TTL:
            logger.info("使用缓存的搜索结果: %s", query)
            return cached_result
        else:
            # 缓存过期，删除
            del search_cache[cache_key]

    # 每次搜索时创建新的SearchTool实例，确保使用最新的环境变量
    search_tool = SearchTool(backend="hybrid")

    try:
        raw_response = search_tool.run(
            {
                "input": query,
                "backend": search_api,
                "mode": "structured",
                "fetch_full_page": config.fetch_full_page,
                "max_results": 5,
                "max_tokens_per_source": MAX_TOKENS_PER_SOURCE,
                "loop_count": loop_count,
            }
        )
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Search backend %s failed: %s", search_api, exc)
        # 搜索失败时返回空结果，而不是抛出异常
        notices = [f"搜索失败: {str(exc)}"]
        payload: dict[str, Any] = {
            "results": [],
            "backend": search_api,
            "answer": None,
            "notices": notices,
        }
        result = (payload, notices, None, search_api)
        # 缓存失败结果，避免重复失败
        search_cache[cache_key] = (current_time, result)
        # 清理缓存，保持大小限制
        if len(search_cache) > SEARCH_CACHE_MAX_SIZE:
            oldest_key = min(search_cache, key=lambda k: search_cache[k][0])
            del search_cache[oldest_key]
        return result

    if isinstance(raw_response, str):
        notices = [raw_response]
        logger.warning("Search backend %s returned text notice: %s", search_api, raw_response)
        payload: dict[str, Any] = {
            "results": [],
            "backend": search_api,
            "answer": None,
            "notices": notices,
        }
    else:
        payload = raw_response
        notices = list(payload.get("notices") or [])

    backend_label = str(payload.get("backend") or search_api)
    answer_text = payload.get("answer")
    results = payload.get("results", [])

    if notices:
        for notice in notices:
            logger.info("Search notice (%s): %s", backend_label, notice)

    logger.info(
        "Search backend=%s resolved_backend=%s answer=%s results=%s",
        search_api,
        backend_label,
        bool(answer_text),
        len(results),
    )

    # 缓存搜索结果
    result = (payload, notices, answer_text, backend_label)
    search_cache[cache_key] = (current_time, result)
    
    # 清理缓存，保持大小限制
    if len(search_cache) > SEARCH_CACHE_MAX_SIZE:
        oldest_key = min(search_cache, key=lambda k: search_cache[k][0])
        del search_cache[oldest_key]

    return result


def _generate_context_cache_key(search_result: dict[str, Any] | None, answer_text: Optional[str], fetch_full_page: bool) -> str:
    """生成上下文缓存键"""
    import json
    result_str = json.dumps(search_result, sort_keys=True) if search_result else "None"
    answer_str = answer_text or "None"
    cache_input = f"{result_str}:{answer_str}:{fetch_full_page}"
    return hashlib.md5(cache_input.encode()).hexdigest()

# 上下文准备缓存
context_cache: dict[str, tuple[float, tuple[str, str]]] = {}


def prepare_research_context(
    search_result: dict[str, Any] | None,
    answer_text: Optional[str],
    config: Configuration,
) -> tuple[str, str]:
    """Build structured context and source summary for downstream agents."""

    import time
    # 生成缓存键
    cache_key = _generate_context_cache_key(search_result, answer_text, config.fetch_full_page)
    
    # 检查缓存
    current_time = time.time()
    if cache_key in context_cache:
        cache_time, cached_result = context_cache[cache_key]
        if current_time - cache_time < SEARCH_CACHE_TTL:
            logger.info("使用缓存的研究上下文")
            return cached_result
        else:
            # 缓存过期，删除
            del context_cache[cache_key]

    sources_summary = format_sources(search_result)
    context = deduplicate_and_format_sources(
        search_result or {"results": []},
        max_tokens_per_source=MAX_TOKENS_PER_SOURCE,
        fetch_full_page=config.fetch_full_page,
    )

    if answer_text:
        context = f"AI直接答案：\n{answer_text}\n\n{context}"

    result = (sources_summary, context)
    
    # 缓存结果
    context_cache[cache_key] = (current_time, result)
    
    # 清理缓存，保持大小限制
    if len(context_cache) > SEARCH_CACHE_MAX_SIZE:
        oldest_key = min(context_cache, key=lambda k: context_cache[k][0])
        del context_cache[oldest_key]

    return result
