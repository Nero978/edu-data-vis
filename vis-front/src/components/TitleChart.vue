<script setup>
import { onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
const props = defineProps({ data: Array })
const chartRef = ref(null)
let chartInstance = null

function draw() {
  if (!props.data?.length) return
  const knowledgeCount = props.data.reduce((acc, cur) => {
    acc[cur.knowledge] = (acc[cur.knowledge] || 0) + 1
    return acc
  }, {})
  if (!chartInstance) chartInstance = echarts.init(chartRef.value)
  chartInstance.setOption({
    title: { text: '知识点题目数量' },
    tooltip: {},
    legend: { data: ['题目数'] },
    xAxis: { type: 'category', data: Object.keys(knowledgeCount) },
    yAxis: { type: 'value' },
    series: [{ name: '题目数', type: 'bar', data: Object.values(knowledgeCount) }]
  })
}

onMounted(draw)
watch(() => props.data, draw)
</script>
<template>
  <div ref="chartRef" class="w-full h-[400px] bg-gradient-to-b from-blue-100 to-white rounded-lg shadow-md p-2 flex items-center justify-center"></div>
</template>
