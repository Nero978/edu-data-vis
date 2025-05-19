<script setup>
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
const props = defineProps({ submitRecords: Array })
const chartRef = ref(null)
let chartInstance = null

function draw() {
  if (!props.submitRecords?.length) return
  // 只保留主流编程语言和常见状态
  const langCount = {}
  props.submitRecords.forEach(r => {
    const lang = r.method || '未知'
    langCount[lang] = (langCount[lang] || 0) + 1
  })
  // 只保留出现次数最多的前5种编程语言
  const langs = Object.entries(langCount).sort((a,b)=>b[1]-a[1]).slice(0,5).map(x=>x[0])
  const stateSet = new Set()
  langs.forEach(lang => {
    props.submitRecords.forEach(r => {
      if ((r.method || '未知') === lang) stateSet.add(r.state || '未知')
    })
  })
  const states = Array.from(stateSet)
  // 构建箱线图数据：每个编程语言下每种状态的用时分布
  const boxData = []
  const series = []
  langs.forEach(lang => {
    states.forEach(state => {
      const arr = props.submitRecords.filter(r => (r.method||'未知')===lang && (r.state||'未知')===state)
        .map(r => Number(r.timeconsume)||0).filter(x=>x>0) // 单位为ms
      if(arr.length>0) boxData.push({lang, state, arr})
    })
  })
  // 每个状态一组
  states.forEach((state, idx) => {
    series.push({
      name: state,
      type: 'boxplot',
      data: langs.map(lang => {
        const found = boxData.find(d => d.lang===lang && d.state===state)
        return found ? found.arr : []
      }),
      boxWidth: [10,30]
    })
  })
  if (!chartInstance) chartInstance = echarts.init(chartRef.value)
  chartInstance.setOption({
    title: { text: '各编程语言下不同答题状态的用时分布', left: 'center' },
    legend: { data: states, top: 30 },
    tooltip: { trigger: 'item' },
    xAxis: { name: '编程语言', type: 'category', data: langs },
    yAxis: { name: '用时(ms)', type: 'value' },
    series
  })
}

onMounted(draw)
watch(() => props.submitRecords, draw)
</script>
<template>
  <div ref="chartRef" class="w-full h-[400px] bg-gradient-to-b from-blue-100 to-white rounded-lg shadow-md p-2 flex items-center justify-center"></div>
</template>
