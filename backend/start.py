#!/usr/bin/env python3

import uvicorn
import os
import sys
from pathlib import Path

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

def main():
    env_path = os.path.join(os.path.dirname(backend_dir), '.env')
    if os.path.exists(env_path):
        from dotenv import load_dotenv
        load_dotenv(env_path)

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(backend_dir)],
        log_level="info"
    )

if __name__ == "__main__":
    main()
