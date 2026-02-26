from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.user import router as user_router
from app.database.db import Base, engine
from app.models.user import User
from app.routes.auth import router as auth_router 
from app.routes import sleep


from app.routes import auth, user, water, mood, exercise



# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Wellness Manager API")
app.include_router(auth_router)
app.include_router(health_router)
app.include_router(user_router)
app.include_router(sleep.router)
app.include_router(water.router)
app.include_router(mood.router)
app.include_router(exercise.router)

@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}