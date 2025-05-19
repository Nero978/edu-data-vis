<script setup>
import { ref, onMounted } from 'vue'
import GenderChart from './components/GenderChart.vue'
import TitleChart from './components/TitleChart.vue'
import SubmitChart from './components/SubmitChart.vue'
import KnowledgeMasteryChart from './components/KnowledgeMasteryChart.vue'
import UserProfileCharts from './components/UserProfileCharts.vue'
import LangKnowledgeChart from './components/LangKnowledgeChart.vue'
import StudentMajorAgeChart from './components/StudentMajorAgeChart.vue'
import DifficultUnreasonableChart from './components/DifficultUnreasonableChart.vue'
import TitleScoreChart from './components/TitleScoreChart.vue'
import TitleKnowledgeGraph from './components/TitleKnowledgeGraph.vue'
import StateTimeMemoryChart from './components/StateTimeMemoryChart.vue'

const studentData = ref([])
const titleData = ref([])
const submitRecords = ref([])
const knowledgeMastery = ref([])
const userProfile = ref({})
const modeMastery = ref([])
const langs = ref([])

onMounted(async () => {
  const [studentRes, titleRes, submitRes] = await Promise.all([
    fetch('http://localhost:8000/api/studentinfo'),
    fetch('http://localhost:8000/api/titleinfo'),
    fetch('http://localhost:8000/api/submitrecords')
  ])
  studentData.value = await studentRes.json()
  titleData.value = await titleRes.json()
  submitRecords.value = await submitRes.json()
  analyzeKnowledgeMastery()
  analyzeUserProfile()
  analyzeModeMastery()
})

function analyzeKnowledgeMastery() {
  if (!submitRecords.value.length || !titleData.value.length) return
  const titleId2Knowledge = {}
  titleData.value.forEach(item => {
    titleId2Knowledge[item.title_ID] = item.knowledge
  })
  const knowledgeStats = {}
  submitRecords.value.forEach(record => {
    const knowledge = titleId2Knowledge[record.title_ID]
    if (!knowledge) return
    if (!knowledgeStats[knowledge]) {
      knowledgeStats[knowledge] = { total: 0, correct: 0, score: 0, count: 0, stateCount: {} }
    }
    knowledgeStats[knowledge].total += 1
    knowledgeStats[knowledge].score += Number(record.score)
    knowledgeStats[knowledge].count += 1
    const state = record.state
    knowledgeStats[knowledge].stateCount[state] = (knowledgeStats[knowledge].stateCount[state] || 0) + 1
    if (state === 'Absolutely_Correct') knowledgeStats[knowledge].correct += 1
  })
  knowledgeMastery.value = Object.entries(knowledgeStats).map(([k, v]) => ({
    knowledge: k,
    avgScore: v.score / v.count,
    correctRate: v.correct / v.total,
    ...v.stateCount
  }))
}

function analyzeUserProfile() {
  if (!submitRecords.value.length || !titleData.value.length) return
  const hourCount = Array(24).fill(0)
  submitRecords.value.forEach(record => {
    const ts = Number(record.time)
    if (!isNaN(ts)) {
      const date = new Date(ts * 1000)
      const hour = date.getHours()
      hourCount[hour]++
    }
  })
  const typeCount = {}
  const titleId2Type = {}
  titleData.value.forEach(item => {
    titleId2Type[item.title_ID] = item.score
  })
  submitRecords.value.forEach(record => {
    const type = titleId2Type[record.title_ID] || '未知'
    typeCount[type] = (typeCount[type] || 0) + 1
  })
  let correct = 0, total = 0
  submitRecords.value.forEach(record => {
    if (record.state === 'Absolutely_Correct') correct++
    total++
  })
  userProfile.value = {
    hourCount,
    typeCount,
    correctRate: total ? correct / total : 0
  }
}

function analyzeModeMastery() {
  if (!submitRecords.value.length || !titleData.value.length) return
  const titleId2Knowledge = {}
  titleData.value.forEach(item => {
    titleId2Knowledge[item.title_ID] = item.knowledge
  })
  const langStats = {}
  submitRecords.value.forEach(record => {
    const lang = record.method || '未知'
    const knowledge = titleId2Knowledge[record.title_ID]
    if (!knowledge) return
    if (!langStats[lang]) langStats[lang] = {}
    if (!langStats[lang][knowledge]) langStats[lang][knowledge] = { total: 0, correct: 0 }
    langStats[lang][knowledge].total += 1
    if (record.state === 'Absolutely_Correct') langStats[lang][knowledge].correct += 1
  })
  const allLangs = Object.keys(langStats)
  const allKnowledges = Array.from(new Set(
    [].concat(...allLangs.map(l => Object.keys(langStats[l])))
  ))
  modeMastery.value = allKnowledges.map(knowledge => {
    const obj = { knowledge }
    allLangs.forEach(lang => {
      const stat = langStats[lang][knowledge]
      obj[lang] = stat ? (stat.correct / stat.total) : null
    })
    return obj
  })
  langs.value = allLangs
}
</script>

<template>
  <div class="bg-gradient-to-b from-blue-50 to-white min-h-screen pb-16">
    <div class="max-w-5xl mx-auto px-4 py-6">
      <h1 class="text-3xl font-bold text-center text-blue-700 mb-8 tracking-wide drop-shadow">教育数据可视化分析系统</h1>
      <section class="mb-8">
        <h2 class="text-xl font-semibold text-blue-600 mb-2">学生性别比例可视化</h2>
        <div class="bg-white rounded-lg shadow p-4"><GenderChart :data="studentData" /></div>
      </section>
      <section class="mb-8">
        <h2 class="text-xl font-semibold text-blue-600 mb-2">学生专业与年龄分布</h2>
        <div class="bg-white rounded-lg shadow p-4"><StudentMajorAgeChart :data="studentData" /></div>
      </section>
      <section class="mb-8">
        <h2 class="text-xl font-semibold text-blue-600 mb-2">知识点题目数量可视化</h2>
        <div class="bg-white rounded-lg shadow p-4"><TitleChart :data="titleData" /></div>
      </section>
      <section class="mb-8">
        <h2 class="text-xl font-semibold text-blue-600 mb-2">题目分数分布与知识点-分数热力图</h2>
        <div class="bg-white rounded-lg shadow p-4"><TitleScoreChart :titleData="titleData" /></div>
      </section>
      <section class="mb-8">
        <h2 class="text-xl font-semibold text-blue-600 mb-2">题目-知识点-从属知识点关系图</h2>
        <div class="bg-white rounded-lg shadow p-4"><TitleKnowledgeGraph :titleData="titleData" /></div>
      </section>
      <section class="mb-8">
        <h2 class="text-xl font-semibold text-blue-600 mb-2">各班级提交总数可视化</h2>
        <div class="bg-white rounded-lg shadow p-4"><SubmitChart :data="submitRecords" /></div>
      </section>
      <section class="mb-8">
        <h2 class="text-xl font-semibold text-blue-600 mb-2">知识点掌握度评估</h2>
        <div class="bg-white rounded-lg shadow p-4"><KnowledgeMasteryChart :data="knowledgeMastery" /></div>
      </section>
      <section class="mb-8">
        <h2 class="text-xl font-semibold text-blue-600 mb-2">学习者画像分析</h2>
        <div class="bg-white rounded-lg shadow p-4"><UserProfileCharts :data="userProfile" /></div>
      </section>
      <section class="mb-8">
        <h2 class="text-xl font-semibold text-blue-600 mb-2">各编程语言下不同答题状态的用时分布</h2>
        <div class="bg-white rounded-lg shadow p-4"><StateTimeMemoryChart :submitRecords="submitRecords" /></div>
      </section>
      <section class="mb-8">
        <h2 class="text-xl font-semibold text-blue-600 mb-2">编程语言与知识掌握程度关系</h2>
        <div class="bg-white rounded-lg shadow p-4"><LangKnowledgeChart :data="modeMastery" :langs="langs" /></div>
        <div class="text-gray-600 text-sm mt-2">
          <b>简要分析：</b>不同编程语言（method字段）下，各知识点的正确率曲线如上图所示。某些编程语言在大多数知识点上表现出更高的正确率，说明其有助于知识的深度理解和长期记忆。若某编程语言在部分知识点上正确率偏低，提示该语言下对相关知识的掌握存在薄弱环节，可针对性优化学习内容或教学策略。
        </div>
      </section>
      <section class="mb-8">
        <h2 class="text-xl font-semibold text-blue-600 mb-2">题目难度与答题者知识掌握度关系</h2>
        <div class="bg-white rounded-lg shadow p-4"><DifficultUnreasonableChart :submitRecords="submitRecords" :titleData="titleData" /></div>
      </section>
    </div>
  </div>
</template>