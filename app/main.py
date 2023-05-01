from fastapi import FastAPI, Depends
from starlette import status

from app.auth.deps import get_current_active_admin, get_current_active_user
from app.routers.admin import router as admin_router
from app.routers.login import router as login
from app.routers.user import router as user_router

app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK)
async def home():
    return "FastAPI + MongoDB"


app.include_router(login, prefix='/auth', tags=['Authentication'])
app.include_router(admin_router, prefix="/admin", tags=['Admin'], dependencies=[Depends(get_current_active_admin)])
# app.include_router(user_router, prefix="/users", tags=['Users'], dependencies=[Depends(get_current_active_user)])
app.include_router(user_router, prefix="/users", tags=['Users'])
