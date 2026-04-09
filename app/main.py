from fastapi import FastAPI
from app.core.config import settings
from app.api.user import router as user_router
from app.api.auth import router as auth_router
from app.api.workspace import router as workspace_router
from app.api.membership import router as membership_router
from app.api.project import router as project_router
from app.api import tasks


app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(workspace_router)
app.include_router(membership_router)
app.include_router(project_router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}


@app.get("/health")
def health_check():
    return {"status": "ok"}