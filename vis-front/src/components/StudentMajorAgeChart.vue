<script setup>
import { onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
const props = defineProps({ data: Array })
const majorRef = ref(null)
const ageRef = ref(null)
let majorChart = null
let ageChart = null

function drawMajor() {
  if (!props.data?.length) return
  const majorCount = props.data.reduce((acc, cur) => {
    const major = cur['major']
    if (major) acc[major] = (acc[major] || 0) + 1
    return acc
  }, {})
  if (!majorChart) majorChart = echarts.init(majorRef.value)
  majorChart.setOption({
    title: { text: '学生专业分布', left: 'center' },
    tooltip: { trigger: 'item' },
    legend: { orient: 'vertical', left: 'left' },
    series: [{
      name: '人数',
      type: 'pie',
      radius: '60%',
      data: Object.entries(majorCount).map(([name, value]) => ({ name, value })),
      emphasis: {
        itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 0, 0, 0.5)' }
      }
    }]
  })
}

function drawAge() {
  if (!props.data?.length) return
  const ageCount = props.data.reduce((acc, cur) => {
    const age = cur['age']
    if (age) acc[age] = (acc[age] || 0) + 1
    return acc
  }, {})
  // 按年龄升序
  const ages = Object.keys(ageCount).map(Number).sort((a, b) => a - b)
  if (!ageChart) ageChart = echarts.init(ageRef.value)
  ageChart.setOption({
    title: { text: '学生年龄分布', left: 'center' },
    tooltip: {},
    xAxis: { type: 'category', data: ages.map(String) },
    yAxis: { type: 'value' },
    series: [{ name: '人数', type: 'bar', data: ages.map(a => ageCount[a]) }]
  })
}

onMounted(() => { drawMajor(); drawAge() })
watch(() => props.data, () => { drawMajor(); drawAge() })
</script>
<template>
  <div style="display:flex;gap:32px;flex-wrap:wrap">
    <div ref="majorRef" class="w-full h-[400px] bg-gradient-to-b from-blue-100 to-white rounded-lg shadow-md p-2 flex items-center justify-center"></div>
    <div ref="ageRef" class="w-full h-[400px] bg-gradient-to-b from-blue-100 to-white rounded-lg shadow-md p-2 flex items-center justify-center"></div>
  </div>
</template>
