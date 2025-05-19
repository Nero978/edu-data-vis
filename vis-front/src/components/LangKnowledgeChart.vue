<script setup>
import { onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
const props = defineProps({ data: Array, langs: Array })
const chartRef = ref(null)
let chartInstance = null

function draw() {
  if (!props.data?.length || !props.langs?.length) return
  if (!chartInstance) chartInstance = echarts.init(chartRef.value)
  chartInstance.setOption({
    title: { text: '编程语言与知识掌握程度关系', top: 0 },
    tooltip: { trigger: 'axis' },
    legend: { data: props.langs, top: 50 },
    xAxis: { type: 'category', data: props.data.map(i => i.knowledge) },
    yAxis: { type: 'value', min: 18, max: 35, name: '正确率(%)' },
    series: props.langs.map(lang => ({
      name: lang,
      type: 'line',
      data: props.data.map(i => i[lang] != null ? (i[lang] * 100).toFixed(2) : null)
    }))
  })
}

onMounted(draw)
watch([() => props.data, () => props.langs], draw)
</script>
<template>
  <div ref="chartRef" class="w-full h-[400px] bg-gradient-to-b from-blue-100 to-white rounded-lg shadow-md p-2 flex items-center justify-center"></div>
</template>
