<template>
  <section class="panel panel-form panel-centered">
    <header class="panel-head">
      <div class="logo">
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path
            d="M12 2.5c-.7 0-1.4.2-2 .6L4.6 7C3.6 7.6 3 8.7 3 9.9v4.2c0 1.2.6 2.3 1.6 2.9l5.4 3.9c1.2.8 2.8.8 4 0l5.4-3.9c1-.7 1.6-1.7 1.6-2.9V9.9c0-1.2-.6-2.3-1.6-2.9L14 3.1a3.6 3.6 0 0 0-2-.6Z"
          />
        </svg>
      </div>
      <div>
        <h1>深度研究助手</h1>
        <p>结合多轮智能检索与总结，实时呈现洞见与引用。</p>
      </div>
    </header>

    <form class="form" @submit.prevent="$emit('submit')">
      <label class="field">
        <span>研究主题</span>
        <textarea
          v-model="localTopic"
          placeholder="例如：探索多模态模型在 2025 年的关键突破"
          rows="4"
          required
        ></textarea>
      </label>

      <section class="options">
        <label class="field option">
          <span>搜索引擎</span>
          <select v-model="localSearchApi">
            <option value="">沿用后端配置</option>
            <option
              v-for="option in searchOptions"
              :key="option"
              :value="option"
            >
              {{ option }}
            </option>
          </select>
        </label>
      </section>

      <div class="form-actions">
        <button class="submit" type="submit" :disabled="loading">
          <span class="submit-label">
            <svg
              v-if="loading"
              class="spinner"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <circle cx="12" cy="12" r="9" stroke-width="3" />
            </svg>
            {{ loading ? "研究进行中..." : "开始研究" }}
          </span>
        </button>
        <button
          v-if="loading"
          type="button"
          class="secondary-btn"
          @click="$emit('cancel')"
        >
          取消研究
        </button>
      </div>
    </form>

    <p v-if="error" class="error-chip">
      <svg viewBox="0 0 20 20" aria-hidden="true">
        <path
          d="M10 3.2c-.3 0-.6.2-.8.5L3.4 15c-.4.7.1 1.6.8 1.6h11.6c.7 0 1.2-.9.8-1.6L10.8 3.7c-.2-.3-.5-.5-.8-.5Zm0 4.3c.4 0 .7.3.7.7v4c0 .4-.3.7-.7.7s-.7-.3-.7-.7V8.2c0-.4.3-.7.7-.7Zm0 6.6a1 1 0 1 1 0 2 1 1 0 0 1 0-2Z"
        />
      </svg>
      {{ error }}
    </p>
    <p v-else-if="loading" class="hint muted">
      正在收集线索与证据，实时进展见右侧区域。
    </p>
  </section>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue';

const props = defineProps<{
  loading: boolean;
  error: string;
  topic: string;
  searchApi: string;
}>();

const emit = defineEmits<{
  (e: 'submit'): void;
  (e: 'cancel'): void;
  (e: 'update:topic', value: string): void;
  (e: 'update:searchApi', value: string): void;
}>();

const localTopic = ref(props.topic);
const localSearchApi = ref(props.searchApi);

const searchOptions = [
  "advanced",
  "duckduckgo",
  "tavily",
  "perplexity",
  "searxng"
];

// 监听本地值变化，更新父组件
watch(localTopic, (newValue) => {
  emit('update:topic', newValue);
});

watch(localSearchApi, (newValue) => {
  emit('update:searchApi', newValue);
});
</script>

<style scoped>
.panel-form h1 {
  margin: 0;
  font-size: 26px;
  letter-spacing: 0.01em;
}

.panel-form p {
  margin: 4px 0 0;
  color: #64748b;
  font-size: 13px;
}

.panel-head {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.logo {
  width: 52px;
  height: 52px;
  display: grid;
  place-items: center;
  border-radius: 16px;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  box-shadow: 0 12px 28px rgba(59, 130, 246, 0.4);
}

.logo svg {
  width: 28px;
  height: 28px;
  fill: #f8fafc;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.field span {
  font-weight: 600;
  color: #475569;
}

textarea,
input,
select {
  padding: 14px 16px;
  border-radius: 16px;
  border: 1px solid rgba(148, 163, 184, 0.35);
  background: rgba(255, 255, 255, 0.92);
  color: #1f2937;
  font-size: 14px;
  transition: border-color 0.2s, box-shadow 0.2s, background 0.2s;
}

textarea:focus,
input:focus,
select:focus {
  outline: none;
  border-color: rgba(37, 99, 235, 0.65);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
  background: #ffffff;
}

.options {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.option {
  flex: 1;
  min-width: 140px;
}

.form-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.submit {
  align-self: flex-start;
  padding: 12px 24px;
  border-radius: 16px;
  border: none;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  color: #ffffff;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s, opacity 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  position: relative;
}

.submit-label {
  display: inline-flex;
  align-items: center;
  gap: 10px;
}

.submit .spinner {
  width: 18px;
  height: 18px;
  fill: none;
  stroke: rgba(255, 255, 255, 0.85);
  stroke-linecap: round;
  animation: spin 1s linear infinite;
}

.submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.submit:not(:disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(37, 99, 235, 0.28);
}

.secondary-btn {
  padding: 10px 18px;
  border-radius: 14px;
  background: rgba(148, 163, 184, 0.12);
  border: 1px solid rgba(148, 163, 184, 0.28);
  color: #1f2937;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s ease, border-color 0.2s ease, color 0.2s ease;
}

.secondary-btn:hover {
  background: rgba(148, 163, 184, 0.2);
  border-color: rgba(148, 163, 184, 0.35);
  color: #0f172a;
}

.error-chip {
  margin-top: 16px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  background: rgba(248, 113, 113, 0.12);
  border: 1px solid rgba(248, 113, 113, 0.35);
  border-radius: 14px;
  color: #b91c1c;
  font-size: 14px;
}

.error-chip svg {
  width: 18px;
  height: 18px;
  fill: currentColor;
}

.hint.muted {
  color: #64748b;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>