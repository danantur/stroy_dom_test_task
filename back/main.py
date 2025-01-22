import uvicorn
from fastapi import FastAPI, Request
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse

from db import Base, engine
from users.views import router as user_router
from roles.views import router as role_router

Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(user_router)
app.include_router(role_router)

origins = [
    f"http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Вы на стартовой странице!"}

@app.exception_handler(IntegrityError)
async def unicorn_exception_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=422,
        content={"message": str(exc.orig)},
    )

if __name__ == '__main__':
    uvicorn.run(app, port=3001)
