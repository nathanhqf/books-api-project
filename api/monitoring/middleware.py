"""
Middleware de Monitoramento
"""

import time
from fastapi import Request
from api.monitoring.logger import api_logger

async def log_requests(request: Request, call_next):
    """Middleware para logar todas as requisições"""
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    api_logger.info(
        "Request processed",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "process_time": round(process_time, 3)
        }
    )
    
    response.headers["X-Process-Time"] = str(process_time)
    return response
