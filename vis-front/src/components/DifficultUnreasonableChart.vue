<script setup>
import { onMounted, ref, watch, nextTick, onUnmounted } from 'vue'
import * as echarts from 'echarts'
const props = defineProps({ submitRecords: Array, titleData: Array })
const chartRef = ref(null)
const containerRef = ref(null)
const isVisible = ref(false)
let chartInstance = null
const loading = ref(true)
let observer = null

function draw() {
  loading.value = true
  if (!props.submitRecords?.length || !props.titleData?.length || !chartRef.value) {
    loading.value = false
    return
  }
  // 1. 题目ID到知识点
  const titleId2Knowledge = {}
  props.titleData.forEach(item => {
    titleId2Knowledge[item.title_ID] = item.knowledge
  })
  // 2. 统计每个题目的答题正确率和答题者平均知识掌握度
  // 先统计每个学习者对每个知识点的正确率
  const studentKnowledge = {}
  props.submitRecords.forEach(r => {
    const stu = r.student_ID, k = titleId2Knowledge[r.title_ID]
    if (!stu || !k) return
    if (!studentKnowledge[stu]) studentKnowledge[stu] = {}
    if (!studentKnowledge[stu][k]) studentKnowledge[stu][k] = { total: 0, correct: 0 }
    studentKnowledge[stu][k].total++
    if (r.state === 'Absolutely_Correct') studentKnowledge[stu][k].correct++
  })
  // 计算每个学生对每个知识点的掌握度
  Object.keys(studentKnowledge).forEach(stu => {
    Object.keys(studentKnowledge[stu]).forEach(k => {
      const stat = studentKnowledge[stu][k]
      stat.mastery = stat.total ? stat.correct / stat.total : 0
    })
  })
  // 统计每个题目的答题正确率和答题者平均知识掌握度
  const titleStats = {}
  props.submitRecords.forEach(r => {
    const tid = r.title_ID, stu = r.student_ID, k = titleId2Knowledge[r.title_ID]
    if (!tid || !stu || !k) return
    if (!titleStats[tid]) titleStats[tid] = { correct: 0, total: 0, masterySum: 0, count: 0, knowledge: k }
    titleStats[tid].total++
    if (r.state === 'Absolutely_Correct') titleStats[tid].correct++
    // 该学生对该知识点的掌握度
    const mastery = studentKnowledge[stu][k]?.mastery ?? 0
    titleStats[tid].masterySum += mastery
    titleStats[tid].count++
  })
  // 生成可视化数据
  const scatterData = Object.entries(titleStats).map(([tid, stat]) => ([
    stat.count ? stat.masterySum / stat.count : 0, // avgMastery
    stat.total ? stat.correct / stat.total : 0,    // correctRate
    tid,                                           // 题号
    stat.knowledge                                 // 知识点
  ]))
  // 计算均值作为动态阈值
  const masteryArr = scatterData.map(d => d[0])
  const correctArr = scatterData.map(d => d[1])
  const meanMastery = masteryArr.reduce((a,b) => a+b, 0) / (masteryArr.length || 1)
  const meanCorrect = correctArr.reduce((a,b) => a+b, 0) / (correctArr.length || 1)
  // 3. 绘制散点图
  if (!chartInstance && chartRef.value) chartInstance = echarts.init(chartRef.value)
  if (chartInstance) {
    chartInstance.setOption({
      title: { text: '题目难度与答题者知识掌握度关系', left: 'center' },
      tooltip: { 
        trigger: 'item', 
        formatter: p => `题号: ${p.data[2]}<br/>知识点: ${p.data[3]}<br/>平均掌握度: ${(p.data[0]*100).toFixed(1)}%<br/>正确率: ${(p.data[1]*100).toFixed(1)}%` 
      },
      xAxis: { name: '答题者平均知识掌握度', min: 0.15, max: 0.4 },
      yAxis: { name: '题目正确率', min: 0, max: 0.6 },
      series: [{
        symbolSize: 14,
        data: scatterData,
        type: 'scatter',
        encode: { x: 0, y: 1, tooltip: [2,3,0,1] },
        itemStyle: {
          color: d => (d.data && d.data[0] > meanMastery && d.data[1] < meanCorrect) ? '#e74c3c' : '#3498db'
        },
        label: {
          show: false
        }
      }]
    })
  }
  loading.value = false
}

function tryDraw() {
  if (isVisible.value && chartRef.value) draw()
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

watch([() => props.submitRecords, () => props.titleData], tryDraw)
onUnmounted(() => {
  if (chartInstance) { chartInstance.dispose(); chartInstance = null }
  if (observer) observer.disconnect()
})
</script>
<template>
  <div ref="containerRef" class="w-full h-[400px] bg-gradient-to-b from-blue-100 to-white rounded-lg shadow-md p-2 flex items-center justify-center relative">
    <div ref="chartRef" class="w-full h-full"></div>
    <transition name="fade">
      <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-white/70 z-10">
        <svg class="animate-spin h-8 w-8 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
        </svg>
      </div>
    </transition>
  </div>
  <div style="max-width:900px;margin-top:8px;font-size:14px;">
    <b>可视分析说明：</b> 红色点表示“高掌握低正确率”题目，可能存在难度不合理。可点击点查看题号、知识点、掌握度与正确率。
  </div>
</template>
<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
