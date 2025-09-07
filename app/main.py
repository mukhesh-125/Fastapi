from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.routers.posts import router as posts_router
from app.routers.users import router as users_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(posts_router, prefix='/posts' ,tags=["Posts"])
app.include_router(users_router, prefix='/users' ,tags=["Users"])

@app.get("/")
async def root():
    return {"message": "Hello World"}

