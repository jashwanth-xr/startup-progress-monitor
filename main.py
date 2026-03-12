from fastapi import FastAPI
from database.connection import engine
from database.init_db import main as init_db
from models.startup import Startup   # noqa: F401
from models.metrics import Metrics   # noqa: F401
from api.routes import router

app = FastAPI(
    title="Startup Progress Monitor",
    description="Track and analyze Indian startup performance over time.",
    version="1.0.0"
)

# create tables on startup if they don't exist
init_db()

# register all routes
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Startup Progress Monitor API is running 🚀"}