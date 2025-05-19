<script setup>
import { onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
const props = defineProps({ data: Array })
const chartRef = ref(null)
let chartInstance = null

function draw() {
  if (!props.data?.length) return
  const classCount = props.data.reduce((acc, cur) => {
    acc[cur.class] = (acc[cur.class] || 0) + 1
    return acc
  }, {})
  const classOrder = Array.from({length: 15}, (_, i) => `Class${i+1}`)
  const xData = classOrder.filter(cls => classCount[cls] !== undefined)
  const yData = xData.map(cls => classCount[cls])
  if (!chartInstance) chartInstance = echarts.init(chartRef.value)
  chartInstance.setOption({
    title: { text: '各班级提交总数' },
    tooltip: {},
    legend: { data: ['提交数'] },
    xAxis: { type: 'category', data: xData },
    yAxis: { type: 'value' },
    series: [{ name: '提交数', type: 'bar', data: yData }]
  })
}

onMounted(draw)
watch(() => props.data, draw)
</script>
<template>
  <div ref="chartRef" class="w-full h-[400px] bg-gradient-to-b from-blue-100 to-white rounded-lg shadow-md p-2 flex items-center justify-center"></div>
</template>
