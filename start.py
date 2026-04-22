"""Startup script — reads PORT from env and launches uvicorn.

This avoids Dockerfile CMD shell-expansion issues on Railway.
"""
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"[start.py] Starting uvicorn on 0.0.0.0:{port}")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
    )
