<script setup>
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
const props = defineProps({ titleData: Array })
const chartRef = ref(null)
let chartInstance = null

function draw() {
  if (!props.titleData?.length) return
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
  if (!chartInstance) chartInstance = echarts.init(chartRef.value)
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

onMounted(draw)
watch(() => props.titleData, draw)
</script>
<template>
  <div ref="chartRef" class="w-full h-[600px] bg-gradient-to-b from-blue-100 to-white rounded-lg shadow-md p-2 flex items-center justify-center"></div>
</template>
