<script setup>
import { ref, onMounted, watch, nextTick, onUnmounted } from 'vue'
import * as echarts from 'echarts'
const props = defineProps({ titleData: Array })
const chartRef = ref(null)
const containerRef = ref(null)
const isVisible = ref(false)
let chartInstance = null
const loading = ref(true)
let observer = null

function draw() {
  loading.value = true
  if (!props.titleData?.length || !chartRef.value) {
    loading.value = false
    return
  }
  // 1. 分数分布
  const scoreCount = {}
  // 2. 知识点-分数热力
  const knowledgeSet = new Set()
  const scoreSet = new Set()
  const heatMap = {}

  props.titleData.forEach(item => {
    // 分数分布
    scoreCount[item.score] = (scoreCount[item.score] || 0) + 1
    // 知识点-分数
    knowledgeSet.add(item.knowledge)
    scoreSet.add(item.score)
    const key = item.knowledge + '_' + item.score
    heatMap[key] = (heatMap[key] || 0) + 1
  })

  const scoreArr = Array.from(scoreSet).sort((a, b) => a - b)
  const knowledgeArr = Array.from(knowledgeSet)
  const heatData = []
  knowledgeArr.forEach((k, i) => {
    scoreArr.forEach((s, j) => {
      heatData.push([j, i, heatMap[k + '_' + s] || 0])
    })
  })

  if (!chartInstance && chartRef.value) chartInstance = echarts.init(chartRef.value)
  if (chartInstance) {
    chartInstance.setOption({
      title: [
        { text: '题目分数分布', left: 'center', top: 0 },
        { text: '知识点-分数热力图', left: 'center', top: 380 }
      ],
      grid: [
        { left: 60, right: 30, top: 40, height: 300 },
        { left: 60, right: 30, top: 450, height: 300 }
      ],
      xAxis: [
        { type: 'category', data: scoreArr, gridIndex: 0, name: '分数' },
        { type: 'category', data: scoreArr, gridIndex: 1, name: '分数' }
      ],
      yAxis: [
        { type: 'value', gridIndex: 0, name: '题目数量' },
        { type: 'category', data: knowledgeArr, gridIndex: 1, name: '知识点' }
      ],
      series: [
        {
          type: 'bar',
          xAxisIndex: 0,
          yAxisIndex: 0,
          data: scoreArr.map(s => scoreCount[s] || 0),
          itemStyle: { color: '#4e79a7' }
        },
        {
          type: 'heatmap',
          xAxisIndex: 1,
          yAxisIndex: 1,
          data: heatData,
          label: { show: true },
          itemStyle: { borderColor: '#fff' }
        }
      ],
      visualMap: [{
        min: 0,
        max: Math.max(...heatData.map(d => d[2])),
        calculable: true,
        orient: 'horizontal',
        left: 'center',
        top: 400,
        inRange: { color: ['#e0f3f8', '#abd9e9', '#74add1', '#4575b4', '#313695'] },
        show: true
      }],
      tooltip: { trigger: 'item' }
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

watch(() => props.titleData, tryDraw)
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
