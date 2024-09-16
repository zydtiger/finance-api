"""
Fastapi entry file.

Author: tigerding
Email: zhiyuanding01@gmail.com
Version: 0.1.0
"""

from fastapi import FastAPI
from router import router

app = FastAPI()
app.include_router(router)
