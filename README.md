# 教育数据可视化分析系统

本项目基于 FastAPI（后端）与 Vue3 + ECharts + TailwindCSS（前端）实现，支持多维度、多表教育数据的高性能可视化分析。

## 主要特性
- **后端（FastAPI）**
  - 提供学生信息、题目信息、答题记录等多表数据API，支持大数据量高性能读取（内存缓存+多线程）。
  - 支持跨域，便于前后端分离开发。
- **前端（Vue3 + ECharts + TailwindCSS）**
  - 完全组件化，所有可视化均为独立组件，结构清晰。
  - 支持学生性别、专业、年龄、知识点、班级、答题行为、编程语言等多维度分析。
  - 题目难度与知识掌握度不匹配的异常题目自动高亮。
  - 所有图表均有美观的加载动画，页面整体风格现代美观。
  - 支持懒加载，图表滑动到视窗内才初始化，极大提升性能。

## 目录结构
```
vis-back/         # FastAPI后端
  main.py         # 主后端API
  data/           # 数据文件（csv）
    Data_StudentInfo.csv
    Data_TitleInfo.csv
    Data_SubmitRecord/
      SubmitRecord-Class1.csv ...
vis-front/        # Vue3前端
  src/
    App.vue       # 主页面
    components/   # 所有ECharts可视化组件
      GenderChart.vue
      StudentMajorAgeChart.vue
      TitleChart.vue
      TitleScoreChart.vue
      TitleKnowledgeGraph.vue
      SubmitChart.vue
      KnowledgeMasteryChart.vue
      UserProfileCharts.vue
      StateTimeMemoryChart.vue
      LangKnowledgeChart.vue
      DifficultUnreasonableChart.vue
    assets/tailwind.css
  main.js         # 入口
```

## 快速启动
### 后端（FastAPI）
1. 安装 `uv` 目录：
   ```bash
   pip install uv
   ```

2. 创建虚拟环境：
   ```bash
   uv venv
   ```

2. 激活虚拟环境：
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
    - Linux/Mac:
      ```bash
      source venv/bin/activate
      ```

3. 安装依赖：      
   ```bash
   uv sync
   ```
3. 启动后端服务：
   ```bash
   python run.py
   ```
   默认监听 http://localhost:8000

### 前端（Vue3）
1. 进入 `vis-front` 目录：
   ```bash
   cd vis-front
   ```
2. 安装依赖：
   ```bash
   npm install
   ```
3. 启动前端服务：
   ```bash
   npm run dev
   ```
   默认监听 http://localhost:5173

## 主要可视化功能
- 学生性别比例、专业与年龄分布
- 知识点题目数量、分数分布、知识点-分数热力图
- 题目-知识点-从属知识点关系图
- 各班级提交总数
- 知识点掌握度评估
- 学习者画像（答题高峰时段、题型偏好、全局正确率）
- 各编程语言下不同答题状态的用时分布（箱线图）
- 编程语言与知识掌握程度关系
- 题目难度与答题者知识掌握度关系（异常题目高亮）

## 性能与体验
- 后端大数据量接口高性能，前端所有图表均支持懒加载和加载动画。
- 页面整体美观，分区清晰，交互流畅。

## 扩展建议
- 支持更多维度分析（如年级、学号段、知识点层级钻取等）
- 图表交互联动、导出功能
- 后端API性能进一步提升、数据预处理、异常检测等

---
如有问题或建议，欢迎反馈！
