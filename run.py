# 启动 FastAPI 服务脚本
# 使用 uvicorn 作为 ASGI 服务器

import os

if __name__ == "__main__":
    os.system(".venv\\Scripts\\activate && uvicorn vis-back.main:app --reload --port 8000")
