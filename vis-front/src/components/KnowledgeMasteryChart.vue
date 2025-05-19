<script setup>
import { onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
const props = defineProps({ data: Array })
const chartRef = ref(null)
let chartInstance = null

function draw() {
  if (!props.data?.length) return
  if (!chartInstance) chartInstance = echarts.init(chartRef.value)
  chartInstance.setOption({
    title: { text: '知识点掌握度评估' },
    tooltip: { trigger: 'axis' },
    legend: { data: ['平均分', '正确率'] },
    xAxis: { type: 'category', data: props.data.map(i => i.knowledge) },
    yAxis: [
      { type: 'value', name: '平均分' },
      { type: 'value', name: '正确率', min: 0, max: 1 }
    ],
    series: [
      { name: '平均分', type: 'bar', data: props.data.map(i => i.avgScore), yAxisIndex: 0 },
      { name: '正确率', type: 'line', data: props.data.map(i => i.correctRate), yAxisIndex: 1 }
    ]
  })
}

onMounted(draw)
watch(() => props.data, draw)
</script>
<template>
  <div ref="chartRef" class="w-full h-[400px] bg-gradient-to-b from-blue-100 to-white rounded-lg shadow-md p-2 flex items-center justify-center"></div>
</template>
