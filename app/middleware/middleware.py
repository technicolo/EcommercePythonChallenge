# app/middleware/correlation_id.py
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = str(uuid.uuid4())
        request.state.correlation_id = correlation_id  
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id  
        return response
