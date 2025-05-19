from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import csv
import os
from fastapi.responses import JSONResponse
import glob
import concurrent.futures

app = FastAPI()

# 允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'Data_StudentInfo.csv')

@app.get("/api/studentinfo")
def get_student_info():
    data = []
    with open(DATA_PATH, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # DictReader自动用表头做key
            data.append(row)
    return JSONResponse(content=data)

@app.get("/api/titleinfo")
def get_title_info():
    data = []
    title_path = os.path.join(os.path.dirname(__file__), 'data', 'Data_TitleInfo.csv')
    with open(title_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return JSONResponse(content=data)

# 提交记录缓存
_submit_cache = {
    'mtime': None,
    'files': None,
    'data': None
}

@app.get("/api/submitrecords")
def get_submit_records():
    # 读取所有班级的提交记录，确保按文件名排序，避免部分文件未被读取
    folder = os.path.join(os.path.dirname(__file__), 'data', 'Data_SubmitRecord')
    all_files = sorted(glob.glob(os.path.join(folder, 'SubmitRecord-Class*.csv')))
    # 获取所有文件的修改时间
    mtimes = tuple(os.path.getmtime(f) for f in all_files)
    # 如果文件列表和修改时间都没变，直接返回缓存
    if _submit_cache['files'] == tuple(all_files) and _submit_cache['mtime'] == mtimes:
        return JSONResponse(content=_submit_cache['data'])
    # 多线程读取每个文件
    def read_file(file):
        records = []
        with open(file, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['class_file'] = os.path.basename(file)
                records.append(row)
        return records
    records = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(read_file, all_files))
        for r in results:
            records.extend(r)
    # 更新缓存
    _submit_cache['files'] = tuple(all_files)
    _submit_cache['mtime'] = mtimes
    _submit_cache['data'] = records
    return JSONResponse(content=records)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with uv!"}
