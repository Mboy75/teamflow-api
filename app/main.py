from fastapi import FastAPI, Request
from app.core.config import settings

from app.api.user import router as user_router
from app.api.auth import router as auth_router
from app.api.workspace import router as workspace_router
from app.api.membership import router as membership_router
from app.api.project import router as project_router
from app.api.skills import router as skills_router
from app.api import tasks
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.detail
        },
    )

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(workspace_router)
app.include_router(membership_router)
app.include_router(project_router)
app.include_router(tasks.router)
app.include_router(skills_router)


@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}


@app.get("/health")
def health_check():
    return {"status": "ok"}