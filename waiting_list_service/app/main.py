import psycopg2
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.routers import (
    organizer_router,
    user_router,
)
from app.utils.errors import WaitingListError

app = FastAPI()
app.include_router(organizer_router.router)
app.include_router(user_router.router)


@app.exception_handler(WaitingListError)
async def exception_handler(request: Request, error: WaitingListError):
    return JSONResponse(
        status_code=error.status_code,
        content={"error_code": error.error_code, "title": error.title}
    )

@app.exception_handler(psycopg2.Error)
async def exception_handler(request: Request, error: psycopg2.Error):
    return JSONResponse(
        status_code=500,
        content={"error_code": "PG01", "title": str(error)}
    )


@app.get("/")
async def root():
    return "Waiting List Service"
