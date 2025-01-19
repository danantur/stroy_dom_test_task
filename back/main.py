import time

import uvicorn
from fastapi import FastAPI, Request, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse

from back.db import Base, engine
from back.users.views import router as user_router
from back.roles.views import router as role_router
from settings import SERVER_SETTINGS

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(role_router)


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
    uvicorn.run(app, host=SERVER_SETTINGS["ip"], port=SERVER_SETTINGS["port"])