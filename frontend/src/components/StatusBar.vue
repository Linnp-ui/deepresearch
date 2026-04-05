<template>
  <header class="status-bar">
    <div class="status-main">
      <div class="status-chip" :class="{ active: loading }">
        <span class="dot"></span>
        {{ loading ? "研究进行中" : "研究流程完成" }}
      </div>
      <span class="status-meta">
        任务进度：{{ completedTasks }} / {{ totalTasks }}
        · 阶段记录 {{ progressLogsLength }} 条
      </span>
    </div>
    <div class="status-controls">
      <button class="secondary-btn" @click="$emit('toggleLogs')">
        {{ logsCollapsed ? "展开流程" : "收起流程" }}
      </button>
    </div>
  </header>
</template>

<script lang="ts" setup>
const props = defineProps<{
  loading: boolean;
  completedTasks: number;
  totalTasks: number;
  progressLogsLength: number;
  logsCollapsed: boolean;
}>();

const emit = defineEmits<{
  (e: 'toggleLogs'): void;
}>();
</script>

<style scoped>
.status-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.status-main {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.status-controls {
  display: flex;
  gap: 8px;
}

.status-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(191, 219, 254, 0.28);
  padding: 8px 14px;
  border-radius: 999px;
  font-size: 13px;
  color: #1f2937;
  border: 1px solid rgba(59, 130, 246, 0.35);
  transition: background 0.3s ease, color 0.3s ease;
}

.status-chip.active {
  background: rgba(129, 140, 248, 0.2);
  border-color: rgba(129, 140, 248, 0.4);
  color: #1e293b;
}

.status-chip .dot {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: #2563eb;
  box-shadow: 0 0 12px rgba(37, 99, 235, 0.45);
  animation: pulse 1.8s ease-in-out infinite;
}

.status-meta {
  color: #64748b;
  font-size: 13px;
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

@keyframes pulse {
  0%,
  100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.3);
    opacity: 0.5;
  }
}

@media (max-width: 960px) {
  .status-bar {
    flex-direction: column;
    align-items: flex-start;
  }

  .status-main,
  .status-controls {
    width: 100%;
  }

  .status-controls {
    justify-content: flex-start;
  }
}
</style>