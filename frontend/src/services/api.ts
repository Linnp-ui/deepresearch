const baseURL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:9000";

export interface ResearchRequest {
  topic: string;
  search_api?: string;
}

export interface ResearchStreamEvent {
  type: string;
  [key: string]: unknown;
}

export interface StreamOptions {
  signal?: AbortSignal;
}

// XSS防护：转义HTML特殊字符
function sanitizeInput(input: string): string {
  return input
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// 验证研究请求参数
function validateResearchRequest(payload: ResearchRequest): void {
  if (!payload.topic || payload.topic.trim().length === 0) {
    throw new Error('研究主题不能为空');
  }
  
  if (payload.topic.length > 500) {
    throw new Error('研究主题不能超过500个字符');
  }
  
  // 验证搜索引擎参数
  if (payload.search_api) {
    const validSearchApis = ['advanced', 'duckduckgo', 'tavily', 'perplexity', 'searxng'];
    if (!validSearchApis.includes(payload.search_api)) {
      throw new Error('无效的搜索引擎');
    }
  }
}

export async function runResearchStream(
  payload: ResearchRequest,
  onEvent: (event: ResearchStreamEvent) => void,
  options: StreamOptions = {}): Promise<void> {
  // 验证和清理输入
  validateResearchRequest(payload);
  
  // 清理输入，防止XSS攻击
  const sanitizedPayload = {
    topic: sanitizeInput(payload.topic),
    search_api: payload.search_api ? sanitizeInput(payload.search_api) : undefined
  };
  const response = await fetch(`${baseURL}/research/stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "text/event-stream"
    },
    body: JSON.stringify(sanitizedPayload),
    signal: options.signal
  });

  if (!response.ok) {
    const errorText = await response.text().catch(() => "");
    throw new Error(
      errorText || `研究请求失败，状态码：${response.status}`
    );
  }

  const body = response.body;
  if (!body) {
    throw new Error("浏览器不支持流式响应，无法获取研究进度");
  }

  const reader = body.getReader();
  const decoder = new TextDecoder("utf-8");
  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();
    buffer += decoder.decode(value || new Uint8Array(), { stream: !done });

    let boundary = buffer.indexOf("\n\n");
    while (boundary !== -1) {
      const rawEvent = buffer.slice(0, boundary).trim();
      buffer = buffer.slice(boundary + 2);

      if (rawEvent.startsWith("data:")) {
        const dataPayload = rawEvent.slice(5).trim();
        if (dataPayload) {
          try {
            const event = JSON.parse(dataPayload) as ResearchStreamEvent;
            onEvent(event);

            if (event.type === "error" || event.type === "done") {
              return;
            }
          } catch (error) {
            console.error("解析流式事件失败：", error, dataPayload);
          }
        }
      }

      boundary = buffer.indexOf("\n\n");
    }

    if (done) {
      // 处理可能的尾巴事件
      if (buffer.trim()) {
        const rawEvent = buffer.trim();
        if (rawEvent.startsWith("data:")) {
          const dataPayload = rawEvent.slice(5).trim();
          if (dataPayload) {
            try {
              const event = JSON.parse(dataPayload) as ResearchStreamEvent;
              onEvent(event);
            } catch (error) {
              console.error("解析流式事件失败：", error, dataPayload);
            }
          }
        }
      }
      break;
    }
  }
}
