<script setup>
import { onMounted, ref, watch, nextTick, onUnmounted } from 'vue'
import * as echarts from 'echarts'
const props = defineProps({ data: Array })
const chartRef = ref(null)
let chartInstance = null
const loading = ref(true)

async function draw() {
  loading.value = true
  await nextTick()
  if (!props.data?.length || !chartRef.value) {
    loading.value = false
    return
  }
  const classCount = props.data.reduce((acc, cur) => {
    acc[cur.class] = (acc[cur.class] || 0) + 1
    return acc
  }, {})
  const classOrder = Array.from({length: 15}, (_, i) => `Class${i+1}`)
  const xData = classOrder.filter(cls => classCount[cls] !== undefined)
  const yData = xData.map(cls => classCount[cls])
  if (!chartInstance && chartRef.value) chartInstance = echarts.init(chartRef.value)
  if (chartInstance) {
    chartInstance.setOption({
      title: { text: '各班级提交总数' },
      tooltip: {},
      legend: { data: ['提交数'] },
      xAxis: { type: 'category', data: xData },
      yAxis: { type: 'value' },
      series: [{ name: '提交数', type: 'bar', data: yData }]
    })
  }
  loading.value = false
}

onMounted(draw)
watch(() => props.data, draw)

onUnmounted(() => {
  if (chartInstance) { chartInstance.dispose(); chartInstance = null }
})
</script>
<template>
  <div ref="chartRef" class="w-full h-[400px] bg-gradient-to-b from-blue-100 to-white rounded-lg shadow-md p-2 flex items-center justify-center relative">
    <transition name="fade">
      <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-white/70 z-10">
        <svg class="animate-spin h-8 w-8 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
        </svg>
      </div>
    </transition>
  </div>
</template>
<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
