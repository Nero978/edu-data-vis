<script setup>
import { onMounted, ref, watch, nextTick, onUnmounted } from 'vue'
import * as echarts from 'echarts'
const props = defineProps({ data: Object })
const hourRef = ref(null)
const typeRef = ref(null)
const rateRef = ref(null)
const containerRef = ref(null)
const isVisible = ref(false)
const loading = ref(true)
let hourChart, typeChart, rateChart, observer = null

function draw() {
  loading.value = true
  if (!props.data) {
    loading.value = false
    return
  }
  // 答题高峰时段
  if (!hourChart && hourRef.value) hourChart = echarts.init(hourRef.value)
  if (hourChart) {
    hourChart.setOption({
      title: { text: '答题高峰时段分布' },
      tooltip: {},
      xAxis: { type: 'category', data: Array.from({length:24},(_,i)=>`${i}:00`) },
      yAxis: { type: 'value' },
      series: [{ name: '答题次数', type: 'bar', data: props.data.hourCount || [] }]
    })
  }
  // 偏好题型
  if (!typeChart && typeRef.value) typeChart = echarts.init(typeRef.value)
  if (typeChart) {
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
  }
  // 正确率仪表盘
  if (!rateChart && rateRef.value) rateChart = echarts.init(rateRef.value)
  if (rateChart) {
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
  loading.value = false
}

function tryDraw() {
  if (isVisible.value && hourRef.value && typeRef.value && rateRef.value) draw()
}

onMounted(() => {
  observer = new window.IntersectionObserver(
    entries => {
      if (entries[0].isIntersecting) {
        isVisible.value = true
        draw()
        observer.disconnect()
      }
    },
    { threshold: 0.1 }
  )
  if (containerRef.value) observer.observe(containerRef.value)
})

watch(() => props.data, tryDraw)

onUnmounted(() => {
  if (hourChart) { hourChart.dispose(); hourChart = null }
  if (typeChart) { typeChart.dispose(); typeChart = null }
  if (rateChart) { rateChart.dispose(); rateChart = null }
  if (observer) observer.disconnect()
})
</script>
<template>
  <div ref="containerRef" style="display:flex;gap:24px;flex-wrap:wrap">
    <div ref="hourRef" class="w-full h-[400px] bg-gradient-to-b from-blue-100 to-white rounded-lg shadow-md p-2 flex items-center justify-center relative">
      <transition name="fade">
        <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-white/70 z-10">
          <svg class="animate-spin h-8 w-8 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
          </svg>
        </div>
      </transition>
    </div>
    <div ref="typeRef" class="w-full h-[400px] bg-gradient-to-b from-blue-100 to-white rounded-lg shadow-md p-2 flex items-center justify-center relative">
      <transition name="fade">
        <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-white/70 z-10">
          <svg class="animate-spin h-8 w-8 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
          </svg>
        </div>
      </transition>
    </div>
    <div ref="rateRef" class="w-full h-[400px] bg-gradient-to-b from-blue-100 to-white rounded-lg shadow-md p-2 flex items-center justify-center relative">
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
