# AGENTS.md - Development Guidelines

This document provides guidelines for agentic coding agents working in this repository.

## Project Structure

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

## Build/Lint/Test Commands

### Backend

```bash
# Install dependencies (from backend/)
pip install -e ".[dev]"

# Run linter (ruff)
ruff check src/

# Run type checker
mypy src/

# Run all tests
pytest

# Run a single test
pytest backend/tests/test_main.py::test_health_check

# Run tests with verbose output
pytest -v
```

### Frontend

```bash
# Install dependencies
cd frontend && npm install

# Start development server
npm run dev

# Build for production
npm run build

# Run type check
npx vue-tsc --noEmit

# Run all tests
npm run test

# Run a single test file
npx vitest run frontend/tests/test_ResearchForm.spec.ts

# Run tests in watch mode
npm run test -- --watch
```

## Code Style Guidelines

### Python (Backend)

**Imports:**
- Use `from __future__ import annotations` for forward references
- Sort imports with `ruff check --select I` (isort)
- Group: stdlib → third-party → local (relative imports with `.`)

**Formatting:**
- Follow PEP 8 (enforced by ruff)
- Line length: Up to 88 chars (ruff default)
- Use Black-compatible formatting

**Types:**
- Use Python 3.10+ union syntax: `str | None` (not `Optional[str]`)
- Use type hints for all function signatures
- Run mypy before committing

**Naming:**
- `snake_case` for functions, variables
- `PascalCase` for classes
- `SCREAMING_SNAKE_CASE` for constants

**Error Handling:**
- Use specific exception types
- Include context in error messages
- Log exceptions with `logger.exception()`

**Docstrings:**
- Use Google style (configured in pyproject.toml)
- First line should be imperative mood (D401)

### TypeScript/Vue (Frontend)

**Components:**
- Use `<script setup lang="ts">` syntax
- Define props with `defineProps<{...}>()`
- Define emits with `defineEmits<{...}>()`
- Use Composition API (not Options API)

**Types:**
- Use TypeScript strict mode
- Define interfaces for data structures
- Avoid `any` - use `unknown` if type is uncertain

**Styling:**
- Use scoped styles in components
- Follow existing CSS patterns (BEM-like)
- Use CSS custom properties for theming

**Testing:**
- Use Vitest with @vue/test-utils
- Mock external dependencies
- Test component behavior, not implementation

## Common Development Workflows

### Running the Application

```bash
# Backend
cd backend
uvicorn src.main:app --reload --port 8000

# Frontend
cd frontend
npm run dev
```

### Environment Configuration

Backend uses `.env` file (see `.env` for reference). Key variables:
- `LLM_PROVIDER`: ollama, lmstudio, openai, etc.
- `LLM_MODEL_ID`: Model identifier
- `LLM_API_KEY`: API key (if required)
- `SEARCH_API`: tavily, duckduckgo, perplexity, etc.

## Testing Guidelines

- Write tests for new features
- Tests should be independent and reproducible
- Use descriptive test names that explain the scenario
- Include Chinese comments for test descriptions (as per existing patterns)

