from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

def problem_detail_response(status_code: int, title: str, detail: str, type_: str = "about:blank", instance: str = ""):
    return JSONResponse(
        status_code=status_code,
        content={
            "type": type_,
            "title": title,
            "status": status_code,
            "detail": detail,
            "instance": instance
        }
    )
