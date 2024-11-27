from fastapi import FastAPI
from auth.routes import router as auth_router
from books.routes import router as books_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(books_router, prefix="/library", tags=["Library"])
