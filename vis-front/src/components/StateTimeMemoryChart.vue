<script setup>
import { ref, onMounted, watch, nextTick, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import 'echarts/extension/dataTool'
const props = defineProps({ submitRecords: Array })
const chartRef = ref(null)
const containerRef = ref(null)
const isVisible = ref(false)
let chartInstance = null
const loading = ref(true)
let observer = null
let grouped = null
let langs = []
let states = []

function preprocess() {
  if (!props.submitRecords?.length) return
  // 统计主流编程语言
  const langCount = {}
  props.submitRecords.forEach(r => {
    const lang = r.method || '未知'
    langCount[lang] = (langCount[lang] || 0) + 1
  })
  langs = Object.entries(langCount).sort((a,b)=>b[1]-a[1]).slice(0,5).map(x=>x[0])
  // 统计所有状态
  const stateSet = new Set()
  langs.forEach(lang => {
    props.submitRecords.forEach(r => {
      if ((r.method || '未知') === lang) stateSet.add(r.state || '未知')
    })
  })
  states = Array.from(stateSet)
  // 预聚合：lang-state => 用时数组
  grouped = {}
  langs.forEach(lang => {
    grouped[lang] = {}
    states.forEach(state => {
      grouped[lang][state] = []
    })
  })
  props.submitRecords.forEach(r => {
    const lang = r.method || '未知'
    const state = r.state || '未知'
    if (langs.includes(lang) && states.includes(state)) {
      const t = Number(r.timeconsume)
      if (t > 0) grouped[lang][state].push(t)
    }
  })
}

function draw() {
  loading.value = true
  if (!props.submitRecords?.length || !chartRef.value) {
    loading.value = false
    return
  }
  preprocess()
  const series = states.map(state => ({
    name: state,
    type: 'boxplot',
    data: langs.map(lang => grouped[lang][state]),
    boxWidth: [10,30]
  }))
  if (!chartInstance && chartRef.value) chartInstance = echarts.init(chartRef.value)
  if (chartInstance) {
    chartInstance.setOption({
      title: { text: '各编程语言下不同答题状态的用时分布', left: 'center' },
      legend: { data: states, bottom: 0 },
      tooltip: { trigger: 'item' },
      xAxis: { name: '编程语言', type: 'category', data: langs },
      yAxis: { name: '用时(ms)', type: 'value', max: 15 },
      series
    })
  }
  loading.value = false
}

function tryDraw() {
  if (isVisible.value && chartRef.value) draw()
}

onMounted(() => {
  observer = new window.IntersectionObserver(
    entries => {
      if (entries[0].isIntersecting) {
        isVisible.value = true
        draw()
        observer.disconnect()
      }
    },
    { threshold: 0.1 }
  )
  if (containerRef.value) observer.observe(containerRef.value)
})

watch(() => props.submitRecords, tryDraw)
onUnmounted(() => {
  if (chartInstance) { chartInstance.dispose(); chartInstance = null }
  if (observer) observer.disconnect()
})
</script>
<template>
  <div ref="containerRef" class="w-full h-[400px] bg-gradient-to-b from-blue-100 to-white rounded-lg shadow-md p-2 flex items-center justify-center relative">
    <div ref="chartRef" class="w-full h-full"></div>
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
