<script setup>
import { onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
const props = defineProps({ data: Object })
const hourRef = ref(null)
const typeRef = ref(null)
const rateRef = ref(null)
let hourChart, typeChart, rateChart

function draw() {
  if (!props.data) return
  // 答题高峰时段
  if (!hourChart) hourChart = echarts.init(hourRef.value)
  hourChart.setOption({
    title: { text: '答题高峰时段分布' },
    tooltip: {},
    xAxis: { type: 'category', data: Array.from({length:24},(_,i)=>`${i}:00`) },
    yAxis: { type: 'value' },
    series: [{ name: '答题次数', type: 'bar', data: props.data.hourCount || [] }]
  })
  // 偏好题型
  if (!typeChart) typeChart = echarts.init(typeRef.value)
  const typeKeys = Object.keys(props.data.typeCount || {})
    .map(k => isNaN(Number(k)) ? k : Number(k))
    .sort((a, b) => (isNaN(a) ? 1 : isNaN(b) ? -1 : a - b))
    .map(k => k.toString())
  const typeLabels = typeKeys.map(k => isNaN(Number(k)) ? k : `${k}分`)
  const typeData = typeKeys.map(k => props.data.typeCount[k])
  typeChart.setOption({
    title: { text: '偏好题型分布' },
    tooltip: {},
    xAxis: { type: 'category', data: typeLabels },
    yAxis: { type: 'value' },
    series: [{ name: '答题次数', type: 'bar', data: typeData }]
  })
  // 正确率仪表盘
  if (!rateChart) rateChart = echarts.init(rateRef.value)
  rateChart.setOption({
    title: { text: '全局正确答题率' },
    tooltip: {},
    series: [{
      name: '正确率',
      type: 'gauge',
      min: 0,
      max: 1,
      detail: { formatter: v => (v*100).toFixed(1)+'%' },
      data: [{ value: props.data.correctRate, name: '正确率' }]
    }]
  })
}

onMounted(draw)
watch(() => props.data, draw)
</script>
<template>
  <div style="display:flex;gap:24px;flex-wrap:wrap">
    <div ref="hourRef" class="w-full h-[400px] bg-gradient-to-b from-blue-100 to-white rounded-lg shadow-md p-2 flex items-center justify-center"></div>
    <div ref="typeRef" class="w-full h-[400px] bg-gradient-to-b from-blue-100 to-white rounded-lg shadow-md p-2 flex items-center justify-center"></div>
    <div ref="rateRef" class="w-full h-[400px] bg-gradient-to-b from-blue-100 to-white rounded-lg shadow-md p-2 flex items-center justify-center"></div>
  </div>
</template>
