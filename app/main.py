from fastapi import FastAPI, Depends
from starlette import status
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from app.auth.users import check_is_admin
from app.routers.admin import admin_router
from app.routers.user import router as user_router

app = FastAPI()


@app.get("/")
async def home():
    return Response("FastAPI + MongoDB")


app.include_router(admin_router, tags=['Users'], prefix="/users")
app.include_router(user_router, tags=['Admin'], prefix="/admin", dependencies=[Depends(check_is_admin)])
