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
  // 构建节点和边
  const nodes = []
  const edges = []
  const nodeMap = {}
  // 统计所有知识点与从属知识点的映射
  const knowledge2sub = {}
  props.titleData.forEach(item => {
    if (item.knowledge && item.sub_knowledge) {
      if (!knowledge2sub[item.knowledge]) knowledge2sub[item.knowledge] = new Set()
      knowledge2sub[item.knowledge].add(item.sub_knowledge)
    }
  })
  // 题目节点、从属知识点节点、知识点节点
  props.titleData.forEach(item => {
    // 题目节点
    if (!nodeMap[item.title_ID]) {
      nodes.push({
        id: item.title_ID,
        name: item.title_ID,
        category: 0,
        symbolSize: 30,
        label: { show: false }
      })
      nodeMap[item.title_ID] = true
    }
    // 从属知识点节点
    if (item.sub_knowledge && !nodeMap[item.sub_knowledge]) {
      nodes.push({
        id: item.sub_knowledge,
        name: item.sub_knowledge,
        category: 2,
        symbolSize: 25,
        label: { show: true }
      })
      nodeMap[item.sub_knowledge] = true
    }
    // 知识点节点
    if (item.knowledge && !nodeMap[item.knowledge]) {
      nodes.push({
        id: item.knowledge,
        name: item.knowledge,
        category: 1,
        symbolSize: 40,
        label: { show: true }
      })
      nodeMap[item.knowledge] = true
    }
    // 题目-从属知识点
    if (item.sub_knowledge) {
      edges.push({ source: item.title_ID, target: item.sub_knowledge, value: '考察' })
    }
  })
  // 知识点-从属知识点（大类-子类）
  Object.entries(knowledge2sub).forEach(([k, subSet]) => {
    subSet.forEach(sub => {
      edges.push({ source: k, target: sub, value: '包含' })
    })
  })
  if (!chartInstance && chartRef.value) chartInstance = echarts.init(chartRef.value)
  if (chartInstance) {
    chartInstance.setOption({
      title: { text: '题目-知识点-从属知识点关系图', left: 'center' },
      tooltip: { trigger: 'item' },
      legend: [{
        data: ['题目', '知识点', '从属知识点'],
        top: 30
      }],
      series: [{
        type: 'graph',
        layout: 'force',
        roam: true,
        label: { position: 'right' },
        categories: [
          { name: '题目' },
          { name: '知识点' },
          { name: '从属知识点' }
        ],
        data: nodes,
        links: edges,
        edgeSymbol: ['none', 'arrow'],
        edgeSymbolSize: 8,
        edgeLabel: {
          show: true,
          formatter: p => p.data.value,
          fontSize: 12
        },
        force: {
          repulsion: 200,
          edgeLength: 120
        },
        emphasis: {
          focus: 'adjacency',
          lineStyle: { width: 4 }
        }
      }]
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
  <div ref="containerRef" class="w-full h-[600px] bg-gradient-to-b from-blue-100 to-white rounded-lg shadow-md p-2 flex items-center justify-center relative">
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
