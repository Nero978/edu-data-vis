<script setup>
import { ref, onMounted, watch, nextTick, onUnmounted } from 'vue'
import * as echarts from 'echarts'
const props = defineProps({ submitRecords: Array })
const chartRef = ref(null)
let chartInstance = null
const loading = ref(true)

function draw() {
  loading.value = true
  if (!props.submitRecords?.length || !chartRef.value) {
    loading.value = false
    return
  }
  // 只保留主流编程语言和常见状态
  const langCount = {}
  props.submitRecords.forEach(r => {
    const lang = r.method || '未知'
    langCount[lang] = (langCount[lang] || 0) + 1
  })
  // 只保留出现次数最多的前5种编程语言
  const langs = Object.entries(langCount).sort((a,b)=>b[1]-a[1]).slice(0,5).map(x=>x[0])
  const stateSet = new Set()
  langs.forEach(lang => {
    props.submitRecords.forEach(r => {
      if ((r.method || '未知') === lang) stateSet.add(r.state || '未知')
    })
  })
  const states = Array.from(stateSet)
  // 构建箱线图数据：每个编程语言下每种状态的用时分布
  const boxData = []
  const series = []
  langs.forEach(lang => {
    states.forEach(state => {
      const arr = props.submitRecords.filter(r => (r.method||'未知')===lang && (r.state||'未知')===state)
        .map(r => Number(r.timeconsume)||0).filter(x=>x>0) // 单位为ms
      if(arr.length>0) boxData.push({lang, state, arr})
    })
  })
  // 每个状态一组
  states.forEach((state, idx) => {
    series.push({
      name: state,
      type: 'boxplot',
      data: langs.map(lang => {
        const found = boxData.find(d => d.lang===lang && d.state===state)
        return found ? found.arr : []
      }),
      boxWidth: [10,30]
    })
  })
  if (!chartInstance && chartRef.value) chartInstance = echarts.init(chartRef.value)
  if (chartInstance) {
    chartInstance.setOption({
      title: { text: '各编程语言下不同答题状态的用时分布', left: 'center' },
      legend: { data: states, top: 30 },
      tooltip: { trigger: 'item' },
      xAxis: { name: '编程语言', type: 'category', data: langs },
      yAxis: { name: '用时(ms)', type: 'value' },
      series
    })
  }
  loading.value = false
}

onMounted(draw)
watch(() => props.submitRecords, draw)
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
