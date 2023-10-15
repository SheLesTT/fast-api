from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import post, user, auth, vote
from app.config import Settings

from fastapi.middleware.cors import CORSMiddleware



settings = Settings()



# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router) # goes into post and tries to search there
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World"}



