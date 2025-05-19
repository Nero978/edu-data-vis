<script setup>
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
const props = defineProps({ titleData: Array })
const chartRef = ref(null)
let chartInstance = null

function draw() {
  if (!props.titleData?.length) return
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

  if (!chartInstance) chartInstance = echarts.init(chartRef.value)
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

onMounted(draw)
watch(() => props.titleData, draw)
</script>
<template>
  <div ref="chartRef" class="w-full h-[400px] bg-gradient-to-b from-blue-100 to-white rounded-lg shadow-md p-2 flex items-center justify-center"></div>
</template>
