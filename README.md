# DeepResearch

DeepResearch是一个基于AI的深度研究助手，结合了前端Vue 3和后端FastAPI技术栈，提供智能的网络搜索、信息汇总和研究报告生成功能。

## 项目结构

```
helloagents-deepresearch/
├── backend/           # Python FastAPI backend
│   ├── src/          # Source code
│   │   ├── agent.py          # Deep research orchestrator
│   │   ├── config.py        # Configuration management
│   │   ├── main.py           # FastAPI application
│   │   ├── models.py         # Data models
│   │   ├── prompts.py       # LLM prompts
│   │   ├── utils.py         # Utilities
│   │   └── services/        # Business logic services
│   │       ├── planner.py
│   │       ├── reporter.py
│   │       ├── search.py
│   │       ├── summarizer.py
│   │       └── tool_events.py
│   ├── tests/        # Backend tests
│   └── pyproject.toml
├── frontend/         # Vue 3 + TypeScript frontend
│   ├── src/
│   │   ├── components/      # Vue components
│   │   ├── services/        # API services
│   │   └── App.vue
│   ├── tests/       # Frontend tests
│   └── package.json
└── test_*.py        # Root-level test utilities
```

## 功能特性

- **智能搜索**：集成多种搜索服务（Tavily、DuckDuckGo等）
- **深度研究**：通过多轮搜索和分析，生成全面的研究报告
- **实时进度**：前端实时显示研究进度和任务状态
- **交互式界面**：直观的用户界面，支持输入研究主题和查看结果
- **可配置性**：支持多种LLM模型和搜索服务

## 技术栈

### 后端
- Python 3.10+
- FastAPI
- HelloAgents
- 多种LLM模型支持

### 前端
- Vue 3
- TypeScript
- Vite

## 快速开始

### 后端安装

1. 进入后端目录
   ```bash
   cd backend
   ```

2. 安装依赖
   ```bash
   pip install -e ".[dev]"
   ```

3. 配置环境变量
   - 复制 `.env.example` 文件为 `.env`
   - 填写必要的API密钥和配置信息

4. 启动后端服务
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

### 前端安装

1. 进入前端目录
   ```bash
   cd frontend
   ```

2. 安装依赖
   ```bash
   npm install
   ```

3. 启动开发服务器
   ```bash
   npm run dev
   ```

## 环境配置

### 后端环境变量

主要配置项（见 `.env.example`）：
- `SEARCH_API`：搜索服务提供商（tavily, duckduckgo等）
- `TAVILY_API_KEY`：Tavily搜索API密钥
- `LLM_PROVIDER`：LLM模型提供商
- `LLM_MODEL_ID`：模型ID
- `LLM_API_KEY`：LLM API密钥
- `LLM_BASE_URL`：LLM服务地址

### 前端环境配置

前端默认连接到 `http://localhost:8000` 的后端服务。如需修改，请编辑 `frontend/src/services/api.ts` 文件。

## 运行测试

### 后端测试

```bash
# 运行所有测试
pytest

# 运行单个测试
pytest backend/tests/test_main.py::test_health_check

# 运行测试并显示详细输出
pytest -v
```

### 前端测试

```bash
# 运行所有测试
npm run test

# 运行单个测试文件
npx vitest run frontend/tests/test_ResearchForm.spec.ts

# 运行测试并监视文件变化
npm run test -- --watch
```

## 代码风格

### 后端（Python）
- 遵循 PEP 8 规范
- 使用 Black 格式化
- 使用 mypy 进行类型检查
- 使用 Google 风格的文档字符串

### 前端（Vue/TypeScript）
- 使用 `<script setup lang="ts">` 语法
- 遵循 Composition API
- 使用 TypeScript 严格模式
- 使用 scoped 样式

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 开启 Pull Request

## 许可证

MIT License

## 联系信息

- 项目地址：https://github.com/Linnp-ui/deepresearch
