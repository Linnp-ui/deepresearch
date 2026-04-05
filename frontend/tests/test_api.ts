import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';
import * as api from '../src/services/api';

// 模拟axios
vi.mock('axios');
const mockedAxios = axios as vi.Mocked<typeof axios>;

describe('API服务测试', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('测试submitResearch函数', async () => {
    const mockResponse = {
      data: {
        report_markdown: '测试报告',
        todo_items: []
      }
    };
    mockedAxios.post.mockResolvedValue(mockResponse);

    const result = await api.submitResearch('测试主题');
    expect(result).toEqual(mockResponse.data);
    expect(mockedAxios.post).toHaveBeenCalledWith('/api/research', { topic: '测试主题' });
  });

  it('测试submitResearchStream函数', async () => {
    const mockResponse = {
      data: {}
    };
    mockedAxios.post.mockResolvedValue(mockResponse);

    const onUpdate = vi.fn();
    await api.submitResearchStream('测试主题', onUpdate);
    expect(mockedAxios.post).toHaveBeenCalledWith('/api/research/stream', { topic: '测试主题' }, {
      responseType: 'stream'
    });
  });

  it('测试submitResearch函数错误处理', async () => {
    const error = new Error('网络错误');
    mockedAxios.post.mockRejectedValue(error);

    await expect(api.submitResearch('测试主题')).rejects.toThrow('网络错误');
  });

  it('测试submitResearchStream函数错误处理', async () => {
    const error = new Error('网络错误');
    mockedAxios.post.mockRejectedValue(error);

    const onUpdate = vi.fn();
    await expect(api.submitResearchStream('测试主题', onUpdate)).rejects.toThrow('网络错误');
  });
});