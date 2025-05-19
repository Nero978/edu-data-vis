<script setup>
import { onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
const props = defineProps({ data: Array })
const chartRef = ref(null)
let chartInstance = null

function draw() {
  if (!props.data?.length) return
  const genderCount = props.data.reduce((acc, cur) => {
    const gender = cur['sex']
    if (gender) acc[gender] = (acc[gender] || 0) + 1
    return acc
  }, {})
  if (!chartInstance) chartInstance = echarts.init(chartRef.value)
  chartInstance.setOption({
    title: { text: '学生性别比例' },
    tooltip: {},
    legend: { data: ['人数'] },
    xAxis: { type: 'category', data: Object.keys(genderCount) },
    yAxis: { type: 'value' },
    series: [{ name: '人数', type: 'bar', data: Object.values(genderCount) }]
  })
}

onMounted(draw)
watch(() => props.data, draw)
</script>
<template>
  <div ref="chartRef" class="w-full h-[400px] bg-gradient-to-b from-blue-100 to-white rounded-lg shadow-md p-2 flex items-center justify-center"></div>
</template>
