from fastapi import FastAPI

app = FastAPI(
    title="TeamFlow API",
    description="A simple FastAPI application",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "welcome to TeamFlow API!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}