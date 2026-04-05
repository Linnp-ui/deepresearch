<template>
  <div class="sidebar-header">
    <button class="back-btn" @click="$emit('back')" :disabled="loading">
      <svg viewBox="0 0 24 24" width="20" height="20">
        <path d="M19 12H5M12 19l-7-7 7-7" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      返回
    </button>
    <h2>🔍 深度研究助手</h2>
  </div>

  <div class="research-info">
    <div class="info-item">
      <label>研究主题</label>
      <p class="topic-display">{{ topic }}</p>
    </div>

    <div class="info-item" v-if="searchApi">
      <label>搜索引擎</label>
      <p>{{ searchApi }}</p>
    </div>

    <div class="info-item" v-if="totalTasks > 0">
      <label>研究进度</label>
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: `${(completedTasks / totalTasks) * 100}%` }"></div>
      </div>
      <p class="progress-text">{{ completedTasks }} / {{ totalTasks }} 任务完成</p>
    </div>
  </div>

  <div class="sidebar-actions">
    <button class="new-research-btn" @click="$emit('newResearch')">
      <svg viewBox="0 0 24 24" width="18" height="18">
        <path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/>
      </svg>
      开始新研究
    </button>
  </div>
</template>

<script lang="ts" setup>
const props = defineProps<{
  topic: string;
  searchApi: string;
  totalTasks: number;
  completedTasks: number;
  loading: boolean;
}>();

const emit = defineEmits<{
  (e: 'back'): void;
  (e: 'newResearch'): void;
}>();
</script>

<style scoped>
.sidebar-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  background: rgba(148, 163, 184, 0.12);
  border: 1px solid rgba(148, 163, 184, 0.28);
  border-radius: 14px;
  color: #1f2937;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s ease, border-color 0.2s ease, color 0.2s ease;
}

.back-btn:hover:not(:disabled) {
  background: rgba(148, 163, 184, 0.2);
  border-color: rgba(148, 163, 184, 0.35);
  color: #0f172a;
}

.back-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.sidebar-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
}

.research-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 32px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-item label {
  font-weight: 600;
  color: #475569;
  font-size: 14px;
}

.info-item p {
  margin: 0;
  color: #1f2937;
  font-size: 14px;
  line-height: 1.5;
}

.topic-display {
  word-break: break-word;
  white-space: pre-wrap;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(148, 163, 184, 0.2);
  border-radius: 999px;
  overflow: hidden;
  margin: 8px 0;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  border-radius: 999px;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 13px;
  color: #64748b;
  text-align: right;
}

.sidebar-actions {
  margin-top: auto;
  padding-top: 24px;
  border-top: 1px solid rgba(148, 163, 184, 0.2);
}

.new-research-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 12px 24px;
  border-radius: 16px;
  border: none;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  color: #ffffff;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s, opacity 0.2s;
}

.new-research-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(37, 99, 235, 0.28);
}
</style>