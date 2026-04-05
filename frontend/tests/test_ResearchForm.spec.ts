import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import ResearchForm from '../src/components/ResearchForm.vue';

describe('ResearchForm组件测试', () => {
  let wrapper: any;

  beforeEach(() => {
    wrapper = mount(ResearchForm, {
      props: {
        loading: false
      }
    });
  });

  it('测试组件渲染', () => {
    expect(wrapper.exists()).toBe(true);
    expect(wrapper.find('h1').text()).toBe('HelloAgents 深度研究助手');
    expect(wrapper.find('input[type="text"]').exists()).toBe(true);
    expect(wrapper.find('button').exists()).toBe(true);
  });

  it('测试输入功能', async () => {
    const input = wrapper.find('input[type="text"]');
    await input.setValue('测试主题');
    expect(input.element.value).toBe('测试主题');
  });

  it('测试提交功能', async () => {
    const input = wrapper.find('input[type="text"]');
    await input.setValue('测试主题');
    
    const button = wrapper.find('button');
    await button.trigger('click');
    
    expect(wrapper.emitted('submit')).toBeTruthy();
    expect(wrapper.emitted('submit')?.[0]).toEqual(['测试主题']);
  });

  it('测试加载状态', async () => {
    await wrapper.setProps({ loading: true });
    const button = wrapper.find('button');
    expect(button.text()).toBe('研究中...');
    expect(button.element.disabled).toBe(true);
  });

  it('测试空输入提交', async () => {
    const button = wrapper.find('button');
    await button.trigger('click');
    expect(wrapper.emitted('submit')).toBeFalsy();
  });
});