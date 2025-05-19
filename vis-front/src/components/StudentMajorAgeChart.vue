<script setup>
import { onMounted, ref, watch, nextTick, onUnmounted } from 'vue'
import * as echarts from 'echarts'
const props = defineProps({ data: Array })
const majorRef = ref(null)
const ageRef = ref(null)
let majorChart = null
let ageChart = null
const loading = ref(true)

async function drawMajor() {
  loading.value = true
  await nextTick()
  if (!props.data?.length || !majorRef.value) {
    loading.value = false
    return
  }
  const majorCount = props.data.reduce((acc, cur) => {
    const major = cur['major']
    if (major) acc[major] = (acc[major] || 0) + 1
    return acc
  }, {})
  if (!majorChart && majorRef.value) majorChart = echarts.init(majorRef.value)
  if (majorChart) {
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
  loading.value = false
}

async function drawAge() {
  loading.value = true
  await nextTick()
  if (!props.data?.length || !ageRef.value) {
    loading.value = false
    return
  }
  const ageCount = props.data.reduce((acc, cur) => {
    const age = cur['age']
    if (age) acc[age] = (acc[age] || 0) + 1
    return acc
  }, {})
  // 按年龄升序
  const ages = Object.keys(ageCount).map(Number).sort((a, b) => a - b)
  if (!ageChart && ageRef.value) ageChart = echarts.init(ageRef.value)
  if (ageChart) {
    ageChart.setOption({
      title: { text: '学生年龄分布', left: 'center' },
      tooltip: {},
      xAxis: { type: 'category', data: ages.map(String) },
      yAxis: { type: 'value' },
      series: [{ name: '人数', type: 'bar', data: ages.map(a => ageCount[a]) }]
    })
  }
  loading.value = false
}

onMounted(() => { drawMajor(); drawAge() })
watch(() => props.data, () => { drawMajor(); drawAge() })
onUnmounted(() => {
  if (majorChart) { majorChart.dispose(); majorChart = null }
  if (ageChart) { ageChart.dispose(); ageChart = null }
})
</script>
<template>
  <div style="display:flex;gap:32px;flex-wrap:wrap">
    <div ref="majorRef" class="w-full h-[400px] bg-gradient-to-b from-blue-100 to-white rounded-lg shadow-md p-2 flex items-center justify-center relative">
      <transition name="fade">
        <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-white/70 z-10">
          <svg class="animate-spin h-8 w-8 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
          </svg>
        </div>
      </transition>
    </div>
    <div ref="ageRef" class="w-full h-[400px] bg-gradient-to-b from-blue-100 to-white rounded-lg shadow-md p-2 flex items-center justify-center relative">
      <transition name="fade">
        <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-white/70 z-10">
          <svg class="animate-spin h-8 w-8 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
          </svg>
        </div>
      </transition>
    </div>
  </div>
</template>
<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
